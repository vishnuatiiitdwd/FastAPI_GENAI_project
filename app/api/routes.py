from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status,APIRouter,Response,UploadFile,File,Form,Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from ..api.controllers import auth,rag
from ..api.dbhelper import schemas
from ..api.dbhelper import database
import tempfile
import shutil
from sqlalchemy.orm import Session
from .controllers import users
from pathlib import Path
from fastapi.responses import JSONResponse
get_db = database.get_db
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME")

router = APIRouter()


@router.post("/login_token")
async def login_for_access_token(response:Response,form_data: Annotated[OAuth2PasswordRequestForm,Depends()],db: Session= Depends(get_db))->schemas.Token:
    user = auth.authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username and password",
            headers={"WWW-Authenticate":"Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub":user.username},expires_delta=access_token_expires)
    response.set_cookie(key=SESSION_COOKIE_NAME,value=access_token,httponly=True,secure=True,samesite="lax",max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60)
    return schemas.Token(access_token=access_token,token_type="bearer")

@router.get("/users/me",response_model=schemas.ShowUser)
async def read_users_me(
    current_user: Annotated[schemas.User, Depends(auth.get_current_active_user)],
    db: Session = Depends(get_db)
):
    return current_user

@router.post("/user_create",response_model=schemas.ShowUser)
async def create_user(user: schemas.User,db: Session= Depends(get_db)):
    return users.create(user,db)

@router.post("/user/logout")
async def logout(response:Response):
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"message":"Logged out"}

@router.put("/update_user/{id}",response_model=schemas.User)
async def update_user(id:int,user:schemas.User,current_user: Annotated[schemas.User, Depends(auth.get_current_active_user)],db:Session=Depends(get_db)):
    result_user =  users.update_old_user(id,user,db)
    if not result_user:
        raise HTTPException(status_code=404,detail="User not found")
    return result_user

@router.delete("/delete/user/{id}")
async def delete_user(id:int,current_user: Annotated[schemas.User, Depends(auth.get_current_active_user)],db:Session=Depends(get_db)):
    return users.del_user(id,db)

@router.post("/upload/")
async def upload_audio(current_user: Annotated[schemas.User, Depends(auth.get_current_active_user)],file: UploadFile = File(...), question: str = Form(...)):
    try:
        current_user_role = current_user.base_role
        file_extension = Path(file.filename).suffix
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = temp_file.name
        transcription = rag.rag_response(temp_file_path,question,file_extension,current_user_role)
        shutil.os.remove(temp_file_path)
        return JSONResponse(content={"message": "File uploaded successfully", "generated_answer": transcription})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
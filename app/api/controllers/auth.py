from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from  ..dbhelper import schemas,models, database
from ..helpers import hashing
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
import jwt
from sqlalchemy.orm import Session
SESSION_COOKIE_NAME = "session_token"

get_db = database.get_db

SECRET_KEY = "377d18abea3fd319a51954da1bf84ce8374a55359e634ac461903cdfb494122b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login_token")


def get_user(db, username: str):
    dbuser = db.query(models.User).filter(models.User.username==username).first()
    if dbuser:
        return schemas.User(**dbuser.__dict__)
    return None

def authenticate_user(db,username:str,password:str):
    user = get_user(db,username)
    if not user:
        return False
    if not hashing.verify_password(password,user.password):
        return False
    return user

def create_access_token(data: dict,expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc)+expires_delta
    else:
        expire = datetime.now(timezone.utc)+timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request:Request,db:Session=Depends(get_db)):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exceptions
    user = get_user(db,username=token_data.username)
    if user is None:
        raise credentials_exceptions
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    if not current_user:
        raise HTTPException(status_code=404, detail="Not an user")
    return current_user



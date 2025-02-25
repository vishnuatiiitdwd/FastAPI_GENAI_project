from ..dbhelper import schemas
from ..dbhelper import models
from sqlalchemy.orm import Session
from ..helpers import hashing
from fastapi import HTTPException

def create(request: schemas.User, db:Session):
    dbuser = db.query(models.User).filter(models.User.username==request.username).first()
    new_user = models.User(username=request.username, email=request.email, password=hashing.get_hash_password(request.password),base_role=request.base_role,auth_role="user")
    if not new_user:
        raise HTTPException(status_code=422,detail="Unprocessable entity")
    if dbuser:
        raise HTTPException(status_code=409,detail="User already exists")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_old_user(id,user:schemas.User,db:Session):
    dbuser = db.query(models.User).filter(models.User.id==id).first()
    if not dbuser:
        return None
    if user.username:
        dbuser.username = user.username
    if user.password:
        dbuser.password = user.password
    if user.base_role:
        dbuser.base_role = user.base_role
    if user.email:
        dbuser.email = user.email
    db.commit()
    db.refresh(dbuser)
    return dbuser

def del_user(id:int, db:Session):
    user=db.query(models.User).filter(models.User.id==id)
    if not user.first:
        raise HTTPException(status_code=404,
                            detail=f"user with {id} not found")
    
    user.delete(synchronize_session=False)
    db.commit()
    return f'User with Id {id} deleted'




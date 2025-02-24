from pydantic import BaseModel
from enum import Enum

class Base_role(str,Enum):
    doctor = "Doctor"
    lawyer = "Lawyer"
    student = "Student"
    enterprise = "Enterprise"
    banker = "Banker"


class User(BaseModel):
    username: str
    email: str
    password: str
    base_role: Base_role
    auth_role: str

class ShowUser(BaseModel):
    username: str
    email:str
    base_role:str
    class config():
        orm_mode = True

class Login(BaseModel):
    userame: str
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username: str|None = None

class UserInDB(User):
    hashed_password: str
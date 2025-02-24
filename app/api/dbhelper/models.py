from sqlalchemy import Column,Integer,String,Boolean
from .database import Base
class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    base_role = Column(String)
    auth_role = Column(String,default="user")
    is_deleted = Column(Boolean,default=False) 
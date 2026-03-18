
import string

from sqlalchemy import TIMESTAMP, Column,Integer,String,Boolean,text
from sqlalchemy.orm import declarative_base

Base =declarative_base()
class Post(Base):
    __tablename__="posts"

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,primary_key=False,nullable=False)
    content=Column(String,primary_key=False,nullable=False)
    published=Column(Boolean,server_default="TRUE",nullable=False)
    created_at =Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class User(Base):
    __tablename__="User"
    id=Column(Integer,primary_key=True,nullable=False)
    username=Column(String,primary_key=False,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at =Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
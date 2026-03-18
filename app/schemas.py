import email

from pydantic import BaseModel
from datetime import datetime
## schema 
class PostBase(BaseModel):
    title:str
    content:str
    published: bool =True

class PostCreate(PostBase):
    pass

## response 
class Post(PostBase):
   created_at:datetime
class Config:
        from_attributes = True

class Userinput(BaseModel):
     username:str
     email:str
     password:str 
## response schema for users table 
class User(BaseModel):
    username:str
    email:str
    created_at:datetime
    class Config:
        from_attributes = True
     
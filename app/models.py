from .database import Base
from sqlalchemy import TIMESTAMP, Column,Integer,String,Boolean,text


class post(Base):
    __tablename__="posts"

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,primary_key=False,nullable=False)
    content=Column(String,primary_key=False,nullable=False)
    published=Column(Boolean,server_default="TRUE",nullable=False)
    created_at =Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))


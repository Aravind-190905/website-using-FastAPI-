from sqlalchemy.orm import Session 
from sqlalchemy import create_engine
from sqlalchemy.orm  import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  # reads your .env file

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine=create_engine(SQLALCHEMY_DATABASE_URL)

#this is the sessionmaker class 

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine) # this is a class btw know more about "factory classes"

Base =declarative_base()

## lets define our tables using python in model.py

def get_db():
    db = SessionLocal()
    try:
        yield db  # This "yields" the session to the route
    finally:
        db.close() # This runs AFTER the response is sent






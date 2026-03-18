from sqlalchemy.exc import IntegrityError
from typing import List
from fastapi import Query, Response,status,HTTPException,Depends
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from . database import engine,SessionLocal,get_db
from . import schemas

models.Base.metadata.create_all(bind=engine) #It essentially tells SQLAlchemy: "Look at all the classes I’ve defined as database models and create the corresponding tables in my actual database if they don't already exist."
app= FastAPI()  # we import the FastAPI class and make an object 




    ## how we could connect to postgresql database 
while(True):
    try:
        conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='asdf',cursor_factory=RealDictCursor)
        cursor=conn.cursor() ##this obj gives us access to the database acts like a terminal.
        print("database connection was successful")
        break
    except Exception as error:
        print("the database failed !!")
        print("the error was !!",error)
        time.sleep(2)

@app.get("/") 
def home():
    return{"message":"this is aravind"}

@app.get("/posts")
def get_posts(db:Session =Depends(get_db)):
    # cursor.execute("""select * from posts""")
    # posts=cursor.fetchall()
    # return{'data':posts}
    posts = db.query(models.Post).all()
    return posts
     

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session = Depends(get_db)):
    # cursor.execute("""insert into posts (title,content,published)values(%s,%s,%s) returning *""",(post.title,post.content,post.published))  ## we have to insert into the database 
    # new_post =cursor.fetchone()
    # conn.commit()
    new_post =models.Post(**post.model_dump()) ##this ** operator unloads the dict.
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    

@app.get("/posts/{id}",response_model=schemas.Post) # this id is a path parameter here.
def get_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("select * from posts where id=(%s)",(id,))
    # post=cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if post is None:
         raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found"
        )
    return post


## delete 
@app.delete("/posts/{id}")
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("delete from posts where id=%s returning *",(id,))
    # post=cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found"
        )
    db.delete(post)
    db.commit()
    return post
    
@app.put("/posts/{id}",response_model=schemas.Post)
def update_posts(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
    # cursor.execute("update posts set title=%s,content=%s,published=%s where id=%s returning *",(post.title,post.content,post.published,id))
    # updated_post=cursor.fetchone()
    #conn.commit()
    query=db.query(models.Post).filter(models.Post.id==id)
    if query.first()==None:
        raise HTTPException(status_code=404, detail="post not found")
    query.update(post.model_dump())
    db.commit()
    return query.first()
   

@app.get("/users",response_model=List[schemas.User])
def get_users(db:Session=Depends(get_db)):
    query=db.query(models.User)
    users=query.all()
    return users

@app.post("/users",response_model=schemas.User)
def create_users(user:schemas.Userinput,db:Session=Depends(get_db)):
    try:
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()          # ← unique constraint checked here
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()        # ← undo the staged changes
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email already exists"
        )

    return new_user
    
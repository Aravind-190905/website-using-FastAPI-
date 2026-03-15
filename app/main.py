from fastapi import Response,status,HTTPException
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time 

app= FastAPI()  # we import the FastAPI class and make an object 

## schema 
class Post(BaseModel):
    title:str
    content:str
    published: bool =True # true here is a default value.
    rating:Optional[int]=None

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
def get_posts():
    cursor.execute("""select * from posts""")
    posts=cursor.fetchall()
    return{'data':posts}
     

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""insert into posts (title,content,published)values(%s,%s,%s) returning *""",(post.title,post.content,post.published))  ## we have to insert into the database 
    new_post =cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}") # this id isa path parameter here.
def get_post(id:int,response:Response):
    cursor.execute("select * from posts where id=(%s)",(id,))
    post=cursor.fetchone()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
    return{'data':post}
## delete 
@app.delete("/posts/{id}")
def delete_post(id:int,response:Response):
    cursor.execute("delete from posts where id=%s returning *",(id,))
    post=cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found"
        )
    return{"data":post}
    
@app.put("/posts/{id}")
def update_posts(id:int,post:Post):
    cursor.execute("update posts set title=%s,content=%s,published=%s where id=%s returning *",(post.title,post.content,post.published,id))
    updated_post=cursor.fetchone()
    if updated_post==None:
        raise HTTPException(status_code=404, detail="post not found")
    conn.commit()
    return{'data':updated_post}
   



    

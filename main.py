from turtle import title
from typing import Optional
from fastapi import FastAPI
from fastapi.params  import Body
from httpx import post
from pydantic import BaseModel
from random import randrange
app= FastAPI()  # we import the FastAPI class and make an object 

## schema 
class Post(BaseModel):
    title:str
    content:str
    published: bool =True # true here is a default value.
    rating:Optional[int]=None

my_posts =[{"title":"title1","content":"post1","id":1},{"title":"favourite food","content":"dosa,idly","id":2}]

@app.get("/")
def home():
    return{"message":"this is aravind"}

@app.get("/posts")
def get_posts():
    return {"data":my_posts} 

@app.post("/posts")
def create_post(post:Post):
    post_dict=post.model_dump()
    post_dict["id"]=randrange(0,1000000)
    my_posts.append(post_dict) # this is to convert the pydantic obj to a dictionary.   
    
    return {"data":my_posts}

@app.get("/posts/{id}") # this id isa path parameter here.
def get_post(id:int):
    print(id)
    for post in my_posts:
        if(post["id"]==id):
            return {"post_details":f"here is the post {post}"}
    

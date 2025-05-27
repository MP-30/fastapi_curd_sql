from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content": "contect of post 1", "id": 1},{"title": "favorite food", "content": "I like pizza", "id": 2}]

@app.get("/")
async def root():
    return {"message" : "Hello World"}


@app.get("/posts")
def get_post():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(1,1000000)
    my_posts.append(post_dict)
    return {"data": post_dict} 


@app.get("/posts/{id}")
def get_post
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg.connect(host = 'localhost', dbname = 'for_wsl_fastapi', user='postgres', password = 'singh', row_factory=dict_row )
        
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as e: 
        print('Database connection failed', e)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "contect of post 1", "id": 1},{"title": "favorite food", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 


@app.get("/")
async def root():
    
    return {"message" : "Hello World"}


@app.get("/posts")
def get_post():
    cursor.execute(" SELECT * FROM posts")
    posts =  cursor.fetchall()
    print("this is for print",posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s,%s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.connect()
    return {"data": new_post} 


@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    single_post = cursor.fetchone()
    print(single_post)
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_details": single_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} does not exist')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published =%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id,)))
    
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    return {'data': updated_post}
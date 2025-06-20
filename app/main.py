from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth
# from .schemas import Post


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root(db: Session = Depends(get_db)):
    
    return {"message" : "Hello World"}



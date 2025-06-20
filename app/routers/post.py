from app import oauth2
from .. import models, schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, get_db
from typing import Optional, List


router = APIRouter(
    prefix="/posts",
    tags=['Post']
)


@router.get("/", response_model= List[schemas.Post])
def get_post(db:Session= Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # cursor.execute(" SELECT * FROM posts")
    # posts =  cursor.fetchall()
    posts = db.query(models.Post).all()
    print("this is for print",posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s,%s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchall()
    # conn.connect()
    
    # print(**post.model_dump())
    print(current_user.email)
    new_post = models.Post(**post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id : int, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    # single_post = cursor.fetchone()
    # print(single_post)
    
    single_post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(single_post)
    
    
    if not single_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return single_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db:Session= Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with {id} does not exist')
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, post:schemas.Post, db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published =%s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id,)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    updated_post_query = db.query(models.Post).filter(models.Post.id == id)
    
    updated_post = updated_post_query.first()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    updated_post_query.update(post.model_dump(), synchronize_session=False)
    
    
    db.commit()
    
    return updated_post_query.first()

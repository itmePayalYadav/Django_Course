import time 
import psycopg2
from . import models
from typing import Optional
from random import randrange
from datetime import datetime
from pydantic import BaseModel
from fastapi.params import Body
from sqlalchemy.orm import Session
from .database import engine, get_db
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = False

while True:
    try:
        con = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='admin@123', cursor_factory=RealDictCursor)
        cursor = con.cursor()
        break
    except Exception as error:
        print(f"Database connection failed {error}")
        time.sleep(2)

@app.get("/")
def root():
    return { "message": "Welcome to the API root"}

@app.get("/posts")
def get_posts(db:Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"message": "All posts retrieved successfully", "posts": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db:Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    # post = cursor.fetchone()
    # con.commit()
    post = models.Post(**post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return {"message": "Post created successfully", "post":post}

@app.get("/posts/{id}")
def get_post_by_id(id:int,  db:Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return { "message": "Post retrieved successfully", "post":post }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db:Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=404, detail="Post not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    db_post = post_query.first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return { "message": "Post updated successfully", "post": post_query.first() }


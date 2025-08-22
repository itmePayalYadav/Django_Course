import time 
import psycopg2
from typing import Optional
from random import randrange
from datetime import datetime
from pydantic import BaseModel
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None
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
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"message": "All posts retrieved successfully", "posts": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    post = cursor.fetchone()
    con.commit()
    return {"message": "Post created successfully", "post":post}

@app.get("/posts/{id}")
def get_post_by_id(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return { "message": "Post retrieved successfully", "post":post }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    con.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s RETURNING * """, (post.title, post.content, post.published, id))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    con.commit()
    return { "message": "Post updated successfully", "post": post }

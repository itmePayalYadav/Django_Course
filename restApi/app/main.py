import time 
import psycopg2
from . import models
from . import schemas
from random import randrange
from datetime import datetime
from fastapi.params import Body
from .utils import hash_Password
from typing import Optional, List
from sqlalchemy.orm import Session
from .database import engine, get_db
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, Response, status, HTTPException, Depends
from .routes import post, user, auth

# ─────────────────────────────
# Database Initialization
# ─────────────────────────────
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog API",
    description="A professional API for managing blog posts and users.",
    version="1.0.0",
    contact={
        "name": "Tejash",
        "url": "https://your-portfolio.com",
        "email": "your@email.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Keep retrying until DB connection succeeds
while True:
    try:
        con = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='admin@123',
            cursor_factory=RealDictCursor
        )
        cursor = con.cursor()
        break
    except Exception as error:
        print(f"Database connection failed {error}")
        time.sleep(2)

# ─────────────────────────────
# Root Endpoint
# ─────────────────────────────

@app.get("/")
def root():
    return {"message": "Welcome to the API root"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

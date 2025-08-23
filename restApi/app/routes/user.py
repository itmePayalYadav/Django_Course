from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..utils import hash_Password
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# ─────────────────────────────
# Users Endpoints
# ─────────────────────────────
@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hash_Password(user.password)
    user_query = models.User(**user.dict())
    db.add(user_query)
    db.commit()
    db.refresh(user_query)
    return user_query

@router.get("/{id}", response_model=schemas.UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


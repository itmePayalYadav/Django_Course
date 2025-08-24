from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db
from ..oauth2 import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=['Authentication']
)

# ─────────────────────────────
# Auth Endpoints
# ─────────────────────────────
@router.post("/login", response_model=schemas.Token)
def loginUser(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    isMatch = utils.verify_password(user_credentials.password, user.password)
    if not isMatch:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Password")
    accessToken = create_access_token({"user_id": user.id})
    return {
        "email": user.email,
        "access_token": accessToken,
        "token_type": "bearer"
    }
    
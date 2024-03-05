from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.models.users import User
from app.schemas import UserCreate, User as UserSchema
from app.schemas.token import Token
from app.core.db import SessionLocal
from passlib.context import CryptContext    
from app.internal.authentication.jwt import create_access_token, create_refresh_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/users/", response_model=Token)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_user = User(
        email=user.email,
        hashed_password=pwd_context.hash(user.password),
        organisation=user.organisation,
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token({"sub": user.email, "organisation": user.organisation})
    refresh_token = create_refresh_token({"sub": user.email, "organisation": user.organisation})
    token_data = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }
    token = Token(**token_data)
    return token



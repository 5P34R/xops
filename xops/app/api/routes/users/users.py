from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import passlib
from passlib.context import CryptContext
from app.models.users import User
from app.schemas.user import UserCreate, User as UserSchema
from app.api.dependencies import get_db

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.get("/users/", response_model=List[UserSchema])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.post("/users/", response_model=UserSchema)
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
    return db_user


@router.get("/users/{user_id}", response_model=UserSchema)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # for now i will not allow the user to change their email and password
    # need to implement password reset 

    # db_user.email = user.email
    db_user.organisation = user.organisation
    # db_user.hashed_password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", response_model=UserSchema)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

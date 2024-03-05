from pydantic import BaseModel

class UserBase(BaseModel):
    id : int | None = None
    email: str
    organisation: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: str

class User(UserBase):
    is_active: bool = True

    class Config:
        orm_mode = True

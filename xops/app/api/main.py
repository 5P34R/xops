from fastapi import APIRouter

from app.api.routes.users import users
from app.api.routes import auth

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
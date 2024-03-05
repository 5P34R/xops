from fastapi import FastAPI
from app.core.config import settings
from app.api.main import router as api_router
from app.core.db import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI()

# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(

#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

app.include_router(api_router, prefix=settings.API_V1_STR)
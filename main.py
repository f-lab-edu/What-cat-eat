from fastapi import FastAPI
from api.v1.endpoints import user
from core.config import settings
from database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(user.router, prefix=settings.API_V1_STR)
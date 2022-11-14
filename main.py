from fastapi import FastAPI
from domain.user import user_router

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

app.include_router(user_router.router)
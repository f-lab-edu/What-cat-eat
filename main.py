from fastapi import FastAPI
from api.endpoints.user import router

app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

app.include_router(router)

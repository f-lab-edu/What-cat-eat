from jose import jwt
from core.config import settings
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/")


def get_current_user_id(token: str = Depends(oauth2_scheme)):
    decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    if not decoded_token["sub"]:
        raise HTTPException(status_code=404, detail="user의 id값을 찾을 수 없습니다.")
    id = int(decoded_token["sub"])

    return id


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from jose import jwt, JWTError
from core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import SessionLocal
from schema.login import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/")


# def get_current_user_id(token: str = Depends(oauth2_scheme)):
#     decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#     if not decoded_token["sub"]:
#         raise HTTPException(status_code=404, detail="user의 id값을 찾을 수 없습니다.")
#     id = int(decoded_token["sub"])

#     return id


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data.user_id


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

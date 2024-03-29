from models.user import User
from passlib.context import CryptContext
from datetime import datetime
from core.config import settings
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from repositories.UserRepository import UserRepository
from fastapi import Depends, HTTPException
from jose import jwt
from schema.login import Login


class LoginService:
    userRepository: UserRepository

    def __init__(self, userRepository: UserRepository = Depends()) -> None:
        self.userRepository = userRepository
        self.user = None

    def verify_password(self, password: str, user_password: str) -> bool:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, user_password)

    def authenticate_user(self, user_id: str, password: str) -> User:
        self.user = self.userRepository.get_user_by_user_id(user_id=user_id)
        if not self.user:
            return None
        if not self.verify_password(password, self.user.password):
            return None
        return self.user

    def create_access_token(
        self, expires_delta: timedelta = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ) -> str:
        expire = datetime.now() + expires_delta
        to_encode = {
            "exp": expire,
            "iss": "what-cat-eat",
            "sub": str(self.user.user_id),
        }
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
        return encoded_jwt

    def login(self, form_data: OAuth2PasswordRequestForm = Depends()) -> Login:
        user = self.authenticate_user(
            user_id=form_data.username, password=form_data.password
        )
        if not user:
            raise HTTPException(status_code=401, detail="아이디나 비밀번호가 틀렸습니다.")

        access_token = self.create_access_token(
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return Login(access_token=access_token, token_type="bearer")

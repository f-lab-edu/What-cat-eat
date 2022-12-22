from repositories.UserRepository import UserRepository
from fastapi import Depends, HTTPException
from schema.user import UserCreate, UserUpdate, validate_password
from models.user import User
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    userRepository: UserRepository

    def __init__(self, userRepository: UserRepository = Depends()) -> None:
        self.userRepository = userRepository

    def get(self, id: int) -> User:
        user = self.userRepository.get(User, id=id)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return user

    def get_user(self, nickname: str, user_id: str) -> User:
        user = self.userRepository.get_value(User, nickname=nickname, user_id=user_id)
        return user

    def create(self, user_body: UserCreate) -> User:
        validate_password(user_body)

        user = self.get_user(user_id=user_body.user_id, nickname=user_body.nickname)
        print(user)
        if user:
            raise HTTPException(
                status_code=409, detail="이미 존재하는 사용자입니다."
            )

        return self.userRepository.create(
            User(
                user_id=user_body.user_id,
                password=pwd_context.hash(user_body.password),
                nickname=user_body.nickname,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        )

    def update(self, id: int, user_body: UserUpdate) -> User:
        user_exist = self.get(id)
        if not user_exist:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

        validate_password(user_body)
        user_body.password = (pwd_context.hash(user_body.password))

        return self.userRepository.update(
            id, User(nickname=user_body.nickname, password=user_body.password)
        )

    def delete(self, id: int):
        user_exist = self.get(id)
        if not user_exist:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return self.userRepository.delete(User, id)

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

    def create(self, user_body: UserCreate) -> User:
        valid_password = validate_password(user_body.password)
        if valid_password.success is True:
            user_body.password = pwd_context.hash(user_body.password)

        else:
            raise HTTPException(
                status_code=valid_password.status_code,
                detail=valid_password.error,
            )

        find_user_by_user_id = self.userRepository.get_user_by_user_id(
            user_id=user_body.user_id
        )
        find_user_by_nickname = self.userRepository.get_user_by_nickname(
            nickname=user_body.nickname
        )

        if find_user_by_user_id | find_user_by_nickname:
            raise HTTPException(status_code=409, detail="이미 존재하는 사용자입니다.")

        return self.userRepository.create(
            User(
                id=user_body.id,
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

        if validate_password(user_body.password):
            user_body.password = pwd_context.hash(user_body.password)

        else:
            raise HTTPException(status_code=400, detail="비밀번호 길이가 너무 짧습니다.")

        return self.userRepository.update(
            id, User(nickname=user_body.nickname, password=user_body.password)
        )

    def delete(self, id: int) -> None:
        user_exist = self.get(id)
        if not user_exist:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        return self.userRepository.delete(User, id)

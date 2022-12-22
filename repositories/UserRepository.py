import abc
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from fastapi import Depends
from models.user import User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> User:
        raise NotImplementedError


class UserRepository(AbstractRepository):
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get(self, user: User, id: int) -> User:
        user = self.db.get(user, id)
        if not user:
            return None
        return user

    def get_value(self, user: User, nickname: str = None, user_id: str = None) -> User:
        user = self.db.query(User).filter(or_(User.nickname == nickname, User.user_id == user_id)).first()
        if not user:
            return None
        return user

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, id: int, user: User) -> User:
        user.id = id
        self.db.merge(user)
        self.db.commit()
        return user

    def delete(self, user: User,  id: int) -> None:
        user = self.db.get(user, id)
        self.db.delete(user)
        self.db.commit()

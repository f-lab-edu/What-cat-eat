import abc
from sqlalchemy.orm import Session
from database import get_db
from fastapi import Depends
from models.user import User


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, model):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, model, id):
        raise NotImplementedError


class UserRepository(AbstractRepository):
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get(self, id: int) -> User:
        user = self.db.get(User, id)
        if not user:
            return None
        return user

    def get_user_by_user_id(self, user_id: str = None) -> User:
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None
        return user

    def get_user_by_nickname(self, nickname: str = None) -> User:
        user = self.db.query(User).filter(User.nickname == nickname).first()
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

    def delete(self, user: User, id: int) -> None:
        user = self.db.get(user, id)
        self.db.delete(user)
        self.db.commit()


class FakeRepository(AbstractRepository):
    def __init__(self):
        self._user = []

    def create(self, user_new: User):
        self._user.append(user_new)
        return self._user[user_new.id - 1]

    def get(self, id: int):
        user = self._user[id - 1]
        if not user:
            return None
        return user

    def get_user_by_user_id(self, user_id: str = None) -> User:
        is_user = None
        for i in self._user:
            if i.user_id == user_id:
                is_user = i
        return is_user

    def get_user_by_nickname(self, nickname: str = None) -> User:
        is_user = None
        for i in self._user:
            if i.nickname == nickname:
                is_user = i
        return is_user

    def update(self, id: int, user_update: User) -> User:
        user = self._user[id - 1]
        user.nickname = user_update.nickname
        user.password = user_update.password
        return user

    def delete(self, user: User, id: int) -> int:
        del self._user[id - 1]
        return len(self._user)

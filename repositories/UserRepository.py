from repositories.RepositoryMeta import AbstractRepository
from sqlalchemy.orm import Session
from api.deps import get_db
from fastapi import Depends
from models.user import User


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

    def update(self, id: int, update_user: User) -> User:
        update_user.id = id
        self.db.merge(update_user)
        self.db.commit()
        return update_user

    def delete(self, id: int) -> None:
        delete_user = self.db.get(User, id)
        self.db.delete(delete_user)
        self.db.commit()


class UserFakeRepository(AbstractRepository):
    def __init__(self):
        self._user = []
        self._user_id = {}
        self._user_nickname = {}
        self.cats = []

    def create(self, user_new: User):
        self._user.append(user_new)
        self._user_id[user_new.user_id] = user_new
        self._user_nickname[user_new.nickname] = user_new
        return self._user[user_new.id - 1]

    def get(self, id: int):
        if len(self._user) < id:
            return None
        user = self._user[id - 1]
        return user

    def get_user_by_user_id(self, user_id: str = None) -> User:
        return self._user_id.get(user_id, None)

    def get_user_by_nickname(self, nickname: str = None) -> User:
        return self._user_nickname.get(nickname, None)

    def update(self, id: int, user_update: User) -> User:
        user = self._user[id - 1]
        del self._user_id[user.user_id]
        del self._user_nickname[user.nickname]
        self._user_id[user_update.user_id] = user_update
        self._user_nickname[user_update.nickname] = user_update
        self._user[id - 1] = user_update
        return user_update

    def delete(self, id: int) -> int:
        delete_user = self._user[id - 1]
        del self._user[id - 1]
        del self._user_id[delete_user.user_id]
        del self._user_nickname[delete_user.nickname]
        return len(self._user)

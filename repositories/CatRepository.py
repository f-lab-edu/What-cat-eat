from repositories.RepositoryMeta import AbstractRepository
from sqlalchemy.orm import Session
from api.deps import get_db
from fastapi import Depends
from models.cat import Cat
from models.user import User


class CatRepository(AbstractRepository):
    db: Session

    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    def get(self, id: int) -> Cat:
        cat = self.db.get(Cat, id)
        if not cat:
            return None
        return cat

    def get_cat_by_user_id(self, user_id: int = None) -> Cat:
        cat = self.db.query(Cat).filter(Cat.user == user_id).first()
        if not cat:
            return None
        return cat

    def get_user_by_user_id(self, current_user_id: str) -> User:
        user = self.db.query(User).filter(User.user_id == current_user_id).first()
        if not user:
            return None
        return user

    def create(self, cat: Cat) -> Cat:
        self.db.add(cat)
        self.db.commit()
        self.db.refresh(cat)
        return cat

    def update(self, id: int, update_cat: Cat) -> Cat:
        update_cat.id = id
        self.db.merge(update_cat)
        self.db.commit()
        return update_cat

    def delete(self, id: int) -> None:
        delete_cat = self.db.get(Cat, id)
        self.db.delete(delete_cat)
        self.db.commit()


class CatFakeRepository(AbstractRepository):
    def __init__(self, user):
        self._cat = []
        self._cat_id = {}
        self.user = user

    def get(self, id: int):
        try:
            cat = self._cat[id - 1]
        except IndexError:
            cat = None
        return cat

    def get_cat_by_user_id(self, user_id: int = None) -> Cat:
        if self._cat.user.id == user_id:
            return self.user.cats

    def get_user_by_user_id(self, current_user_id: str) -> User:
        try:
            return self.user._user_id[current_user_id]
        except KeyError:
            return None

    def create(self, cat: Cat):
        self.user.cats.append(cat)
        self._cat.append(cat)
        self._cat_id[cat.id] = cat
        return self._cat[cat.id - 1]

    def update(self, id: int, cat_update: Cat) -> Cat:
        cat = self._cat[id - 1]
        del self._cat_id[cat.id]
        self._cat_id[cat_update.id] = cat_update
        self._cat[id - 1] = cat_update
        return cat_update

    def delete(self, id: int) -> int:
        delete_cat = self._cat[id - 1]
        del self._cat[id - 1]
        del self._cat_id[delete_cat.id]
        return len(self._cat)


# cat_id를 id로 바꿈 -> 아마 에러날 듯

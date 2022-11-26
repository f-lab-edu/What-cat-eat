from sqlalchemy.orm import Session
from schema.user import UserCreate, UserUpdate
from models.user import User
from passlib.context import CryptContext
from database import get_db
from datetime import datetime
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(id: int, db: Session) -> User:
    user = db.query(User).filter(User.id == id).one_or_none()
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")


def create_user(user_create: UserCreate, db: Session = next(get_db())):
    db_user = User(
        user_id=user_create.user_id,
        password=pwd_context.hash(user_create.password),
        nickname=user_create.nickname,
        created_at=datetime.now(),
    )
    user_create.validate_password(user_create)
    db.add(db_user)
    db.commit()
    return db_user


def update_user(user_update: UserUpdate, id: int, db: Session = next(get_db())):
    user = db.query(User).filter(User.id == id)

    user_update.validate_password(user_update)

    del user_update.password_check
    if user_update.password:
        user_update.password = pwd_context.hash(user_update.password)

    user.update(user_update.dict())
    db.commit()


def delete_user(id: int, db: Session) -> None:
    get_user(id, db)
    db.query(User).filter(User.id == id).delete()
    db.commit()


def get_existing_user(db: Session, user_id: str):
    is_exist_user = db.query(User).filter(User.user_id == user_id).one_or_none()
    if is_exist_user:
        return True
    return False

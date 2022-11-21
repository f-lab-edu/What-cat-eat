from sqlalchemy.orm import Session
from schema.user import UserCreate, UserUpdate
from models.user import User
from passlib.context import CryptContext
from database import get_db
from datetime import datetime


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    return user


def get_existing_user(db: Session, user_create: UserCreate):
    is_exist_user = (
        db.query(User).filter(User.user_id == user_create.user_id).one_or_none()
    )
    if is_exist_user:
        return True
    return False


def get_user(db: Session, id: int):
    user = db.query(User).filter(User.id == id).one_or_none()
    if user:
        return True
    return False

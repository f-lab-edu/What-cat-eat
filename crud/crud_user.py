from sqlalchemy.orm import Session
from schema.user import validate_password, UserCreate, UserUpdate
from models.user import User
from passlib.context import CryptContext
from database import get_db
from datetime import datetime
from fastapi import HTTPException, Depends

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(id: int, db: Session = Depends()) -> User:
    user = db.query(User).filter(User.id == id).one_or_none()
    if not user:
        return None
    return user

    
def get_user_by_nickname(nickname: str, db: Session) -> User:
    user = db.query(User).filter(User.nickname == nickname).one_or_none()
    if not user:
        return None
    return user


def create_user(user_create: UserCreate, db: Session = Depends(get_db())):
    db_user = User(
        user_id=user_create.user_id,
        password=pwd_context.hash(user_create.password),
        nickname=user_create.nickname,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    validate_password(user_create)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(user_update: UserUpdate, id: int, db: Session = Depends(get_db())):
    user = db.query(User).filter(User.id == id)

    validate_password(user_update)

    del user_update.password_check
    if user_update.password:
        user_update.password = pwd_context.hash(user_update.password)

    user.update(user_update.dict())
    db.commit()


def delete_user(id: int, db: Session) -> None:
    user = get_user_by_id(id=id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    db.query(User).filter(User.id == id).delete()
    db.commit()


def get_user_by_user_ID(user_id: str, db: Session):
    user = db.query(User).filter(User.user_id == user_id).one_or_none()
    if not user:
        return None
    return user
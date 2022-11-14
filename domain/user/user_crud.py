from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User
from passlib.context import CryptContext
from database import get_db
from datetime import datetime
from sqlalchemy.sql import text


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(user_create: UserCreate, db: Session=next(get_db())):
    db_user = User(user_id=user_create.user_id,
                    password=pwd_context.hash(user_create.password),
                    nickname=user_create.nickname, created_at=datetime.now())

    db.add(db_user)
    db.commit()

def get_existing_user(db: Session, user_create: UserCreate):
    if db.query(User).filter(text(user_create.user_id)):
        return True
    return False

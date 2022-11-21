from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette import status
from database import get_db
from crud.crud_user import create_user, get_existing_user, update_user
from schema.user import UserCreate, UserUpdate

router = APIRouter(
    prefix="/api/user",
)


@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: UserCreate, db: Session = Depends(get_db)):
    user = get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다."
        )
    create_user(user_create=_user_create, db=db)


@router.put("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def user_update(_user_update: UserUpdate, id: int, db: Session = Depends(get_db)):
    update_user(user_update=_user_update, id=id, db=db)

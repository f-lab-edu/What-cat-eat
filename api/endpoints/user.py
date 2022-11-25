from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from crud.crud_user import (
    create_user,
    get_existing_user,
    update_user,
    get_user,
    delete_user,
)
from schema.user import UserCreate, UserUpdate, UserGet

router = APIRouter(
    prefix="/api/user",
)


@router.get("/{id}/", response_model=UserGet, status_code=status.HTTP_200_OK)
def user_get(id: int, db: Session = Depends(get_db)):
    return get_user(id=id, db=db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def user_create(_user_create: UserCreate, db: Session = Depends(get_db)):
    user = get_existing_user(db, user_create=_user_create.user_id)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다."
        )
    create_user(user_create=_user_create, db=db)
    return {"detail": "사용자가 생성되었습니다."}


@router.put("/{id}/", status_code=status.HTTP_200_OK)
def user_update(_user_update: UserUpdate, id: int, db: Session = Depends(get_db)):
    get_user(id, db)
    update_user(user_update=_user_update, id=id, db=db)
    return {"detail": "수정되었습니다."}


@router.delete("/{id}/", status_code=status.HTTP_200_OK)
def user_delete(id: int, db: Session = Depends(get_db)):
    delete_user(id, db)
    return {"detail": "탈퇴되었습니다."}

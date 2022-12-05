from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from crud.crud_user import (
    create_user,
    update_user,
    get_user_by_id,
    delete_user,
    get_user_by_user_ID,
)
from schema.user import UserCreate, UserUpdate, UserGet

router = APIRouter(
    prefix="/user",
)


@router.get("/{id}/", response_model=UserGet, status_code=status.HTTP_200_OK)
def user_get(id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(id=id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
def user_create(_user_create: UserCreate, db: Session = Depends(get_db)):
    # user_id = _user_create.user_id
    # user = get_user_by_user_ID(db=db, user_id=user_id)
    # if user:
    #     raise HTTPException(
    #         status_code=status.HTTP_409_CONFLICT, detail="이미 존재하는 사용자입니다."
    #     )
    create_user(user_create=_user_create, db=db)
    return {"detail": "사용자가 생성되었습니다."}


@router.put("/{id}/", status_code=status.HTTP_200_OK)
def user_update(_user_update: UserUpdate, id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(id=id, db=db)
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    update_user(user_update=_user_update, id=id, db=db)
    return {"detail": "수정되었습니다."}


@router.delete("/{id}/", status_code=status.HTTP_200_OK)
def user_delete(id: int, db: Session = Depends(get_db)):
    delete_user(id, db)
    return {"detail": "탈퇴되었습니다."}

from fastapi import APIRouter, Depends, HTTPException, status
from services.UserServices import UserService
from schema.user import UserCreate, UserUpdate, UserGet

router = APIRouter(
    prefix="/user",
)


@router.get("/{id}/", response_model=UserGet, status_code=status.HTTP_200_OK)
def get_user(id: int, userService: UserService = Depends()):
    return userService.get(id)


@router.post("/", response_model=UserGet, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, userService: UserService = Depends()):
    return userService.create(user)


@router.put("/{id}/", response_model=UserGet, status_code=status.HTTP_200_OK)
def update_user(id: int, user_body: UserUpdate, userService: UserService = Depends()):
    return userService.update(id, user_body)


@router.delete("/{id}/", status_code=status.HTTP_200_OK)
def delete_user(id: int, userService: UserService = Depends()):
    userService.delete(id)
    return {"detail": "탈퇴되었습니다."}


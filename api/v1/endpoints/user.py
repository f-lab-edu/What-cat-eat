from fastapi import APIRouter, Depends, status
from services.UserServices import UserService
from schema.user import UserCreate, UserUpdate, UserGet
from api.deps import get_current_user_id

router = APIRouter(
    prefix="/user",
)


@router.get("/{id}", response_model=UserGet, status_code=status.HTTP_200_OK)
def get_user(id: int, userService: UserService = Depends()):
    return userService.get(id)


@router.post("", response_model=UserGet, status_code=status.HTTP_201_CREATED)
def create_user(user_body: UserCreate, userService: UserService = Depends()):
    return userService.create(user_body)


@router.put("/{id}", response_model=UserGet, status_code=status.HTTP_200_OK)
def update_user(
    id: int,
    user_body: UserUpdate,
    userService: UserService = Depends(),
    current_user_id: str = Depends(get_current_user_id),
):

    return userService.update(id, user_body, current_user_id)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_user(
    id: int,
    userService: UserService = Depends(),
    current_user_id: str = Depends(get_current_user_id),
):
    userService.delete(id, current_user_id)
    return {"detail": "탈퇴되었습니다."}

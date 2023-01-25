from fastapi import APIRouter, Depends, status
from services.UserServices import UserService
from schema.user import UserCreate, UserUpdate, UserGet
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/")
router = APIRouter(
    prefix="/user",
)


def get_current_user(
    userService: UserService = Depends(), token=Depends(oauth2_scheme)
):
    return userService.get_current_user(token)


@router.get("/{id}/", response_model=UserGet, status_code=status.HTTP_200_OK)
def get_user(id: int, userService: UserService = Depends()):
    return userService.get(id)


@router.post("/", response_model=UserGet, status_code=status.HTTP_201_CREATED)
def create_user(user_body: UserCreate, userService: UserService = Depends()):
    return userService.create(user_body)


@router.put("/{id}/", response_model=UserGet, status_code=status.HTTP_200_OK)
def update_user(
    id: int,
    user_body: UserUpdate,
    userService: UserService = Depends(),
    req_user: str = Depends(get_current_user),
):
    return userService.update(id, user_body, req_user)


@router.delete("/{id}/", status_code=status.HTTP_200_OK)
def delete_user(
    id: int,
    userService: UserService = Depends(),
    req_user: str = Depends(get_current_user),
):
    userService.delete(id, req_user)
    return {"detail": "탈퇴되었습니다."}

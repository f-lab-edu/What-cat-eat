from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from services.LoginService import LoginService
from schema.login import Login

router = APIRouter()


@router.post("/login", response_model=Login, status_code=status.HTTP_200_OK)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    loginService: LoginService = Depends(),
):
    return loginService.login(form_data)

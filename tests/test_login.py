import pytest
from fastapi import HTTPException, Form
from repositories.UserRepository import FakeRepository
from services.UserServices import UserService
from services.LoginService import LoginService
from schema.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm

repository = FakeRepository()


@pytest.fixture
def login_service():
    return LoginService(userRepository=repository)


@pytest.fixture
def user_service():
    return UserService(userRepository=repository)


def test_user_create(user_service):
    id = 1
    user_id = "test_id"
    nickname = "test_nickname"
    password = "test1234"
    user = user_service.create(
        UserCreate(id=id, user_id=user_id, nickname=nickname, password=password)
    )
    assert user.id == 1
    return user


def test_user_id_is_incorrect(login_service):
    username = Form("wrong_id").default
    password = Form("test1234").default
    scope = ""
    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(
            username=username, password=password, scope=scope
        )
        login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_password_is_incorrect(login_service):
    username = Form("test_id").default
    password = Form("wrong_password1").default
    scope = ""
    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(
            username=username, password=password, scope=scope
        )
        login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_user_id_not_entered(login_service):
    username = Form("").default
    password = Form("password").default
    scope = ""

    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(
            username=username, password=password, scope=scope
        )
        login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_password_not_entered(login_service):
    username = Form("test_id").default
    password = Form("").default
    scope = ""

    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(
            username=username, password=password, scope=scope
        )
        login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_user_id_and_password_not_enterd(login_service):
    username = Form("").default
    password = Form("").default
    scope = ""

    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(
            username=username, password=password, scope=scope
        )
        login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_login(login_service):
    username = Form("test_id").default
    password = Form("test1234").default
    scope = ""

    form_data = OAuth2PasswordRequestForm(
        username=username, password=password, scope=scope
    )
    token = login_service.login(form_data)

    assert type(token.access_token) == str
    assert token.token_type == "bearer"

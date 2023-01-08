import pytest
from fastapi import HTTPException
from repositories.UserRepository import FakeRepository
from services.UserServices import UserService
from services.LoginService import LoginService
from schema.user import UserCreate, UserUpdate
from pydantic import ValidationError

@pytest.fixture
def login_service():
    repository = FakeRepository()
    return LoginService(userRepository=repository)

@pytest.fixture
def user_service():
    repository = FakeRepository()
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
    form_data = {
        "username": "test_id",
        "password": "test1234"
    }
    token = login_service.login(form_data)

    assert type(token["access_token"]) == str
    assert token["token_type"] == "bearer"


# def test_password_is_incorrect(user_service):
#     user = test_user_create(user_service)
#     user_get = user_service.get(id=user.id)

#     assert user_get.id == 1
#     assert user_get.user_id == "test_id"


# def test_login_user(user_service):
#     user = test_user_create(user_service)
#     user_get = user_service.get(id=user.id)

#     assert user_get.id == 1
#     assert user_get.user_id == "test_id"
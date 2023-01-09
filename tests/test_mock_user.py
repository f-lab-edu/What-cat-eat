import pytest
from fastapi import HTTPException
from repositories.UserRepository import FakeRepository
from services.UserServices import UserService
from schema.user import UserCreate, UserUpdate
from pydantic import ValidationError


@pytest.fixture
def user_service():
    repository = FakeRepository()
    return UserService(userRepository=repository)


def test_max_length_in_userid(user_service):
    with pytest.raises(ValidationError) as response:
        user_service.create(
            UserCreate(
                id=2,
                user_id="hellozz",
                nickname="testnicknametestnickname",
                password="password1234",
            )
        )
    assert isinstance(response.value, ValidationError)
    # assert response.value


def test_min_length_in_userid(user_service):
    with pytest.raises(ValidationError) as response:
        user_service.create(
            UserCreate(id=2, user_id="hellozz", nickname="", password="password1234")
        )
    assert isinstance(response.value, ValidationError)
    # assert response.value


def test_userid_is_empty(user_service):
    with pytest.raises(ValidationError) as response:
        user_service.create(
            UserCreate(id=2, nickname="test_nickname", password="password1234")
        )
    assert isinstance(response.value, ValidationError)
    # assert response.value


def test_nickname_is_empty(user_service):
    with pytest.raises(ValidationError) as response:
        user_service.create(
            UserCreate(id=2, user_id="test_nickname", password="password1234")
        )
    assert isinstance(response.value, ValidationError)
    # assert response.value


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


def test_get_user(user_service):
    user = test_user_create(user_service)
    user_get = user_service.get(user.id)

    assert user_get.id == 1
    assert user_get.user_id == "test_id"


def test_unique_user_id(user_service):
    test_user_create(user_service)
    with pytest.raises(HTTPException) as response:
        user_service.create(
            UserCreate(
                id=2, user_id="test_id", nickname="hello", password="password1234"
            )
        )

    assert isinstance(response.value, HTTPException)
    assert response.value.status_code == 409
    assert response.value.detail == "이미 존재하는 사용자입니다."


def test_unique_nickname(user_service):
    test_user_create(user_service)
    with pytest.raises(HTTPException) as response:
        user_service.create(
            UserCreate(
                id=2, user_id="hello", nickname="test_nickname", password="password1234"
            )
        )

    assert isinstance(response.value, HTTPException)
    assert response.value.status_code == 409
    assert response.value.detail == "이미 존재하는 사용자입니다."


def test_update_user(user_service):
    user = test_user_create(user_service)
    user_update = user_service.update(
        user.id, UserUpdate(nickname="amend_user", password="test1234")
    )

    assert user_update.nickname == "amend_user"


def test_delete_user(user_service):
    user = test_user_create(user_service)
    count = user_service.delete(user.id)

    assert count == 0

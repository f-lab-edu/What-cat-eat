import pytest
from fastapi import HTTPException
from schema.user import UserCreate, UserUpdate
from pydantic import ValidationError
from tests.conftest import MOCK_TEST_USER, MOCK_TEST_USER_NEW


def test_max_length_in_userid(mock_user_service):
    with pytest.raises(ValidationError) as response:
        mock_user_service.create(
            UserCreate(
                id=2,
                user_id="hellozz",
                nickname="testnicknametestnickname",
                password="password1234",
            )
        )
    assert isinstance(response.value, ValidationError)


def test_min_length_in_userid(mock_user_service):
    with pytest.raises(ValidationError) as response:
        mock_user_service.create(
            UserCreate(id=2, user_id="hellozz", nickname="", password="password1234")
        )
    assert isinstance(response.value, ValidationError)


def test_userid_is_empty(mock_user_service):
    with pytest.raises(ValidationError) as response:
        mock_user_service.create(
            UserCreate(id=2, nickname="test_nickname", password="password1234")
        )
    assert isinstance(response.value, ValidationError)


def test_nickname_is_empty(mock_user_service):
    with pytest.raises(ValidationError) as response:
        mock_user_service.create(
            UserCreate(id=2, user_id="test_nickname", password="password1234")
        )
    assert isinstance(response.value, ValidationError)


def test_get_user(mock_user_service):
    user_get = mock_user_service.get(MOCK_TEST_USER.id)
    assert user_get.id == 1
    assert user_get.user_id == "test_id"


def test_unique_user_id(mock_user_service):
    with pytest.raises(HTTPException) as response:
        mock_user_service.create(
            UserCreate(
                id=2, user_id="test_id", nickname="hello", password="password1234"
            )
        )

    assert isinstance(response.value, HTTPException)
    assert response.value.status_code == 409
    assert response.value.detail == "이미 존재하는 사용자입니다."


def test_unique_nickname(mock_user_service):
    with pytest.raises(HTTPException) as response:
        mock_user_service.create(
            UserCreate(
                id=2, user_id="hello", nickname="test_nickname", password="password1234"
            )
        )

    assert isinstance(response.value, HTTPException)
    assert response.value.status_code == 409
    assert response.value.detail == "이미 존재하는 사용자입니다."


def test_update_another_user(mock_user_service_new):
    with pytest.raises(HTTPException) as response:
        mock_user_service_new.update(
            MOCK_TEST_USER.id,
            UserUpdate(nickname="amend_user", password="test1234"),
            MOCK_TEST_USER_NEW.user_id,
        )

    assert response.value.status_code == 401


def test_update_user(mock_user_service):
    user_update = mock_user_service.update(
        MOCK_TEST_USER.id,
        UserUpdate(nickname="amend_user", password="test1234"),
        MOCK_TEST_USER.user_id,
    )

    assert user_update.nickname == "amend_user"


def test_delete_another_user(mock_user_service_new):
    with pytest.raises(HTTPException) as response:
        mock_user_service_new.delete(MOCK_TEST_USER.id, MOCK_TEST_USER_NEW.user_id)

    assert response.value.status_code == 401


def test_delete_user(mock_user_service):
    count = mock_user_service.delete(MOCK_TEST_USER.id, MOCK_TEST_USER.user_id)

    assert count == 0

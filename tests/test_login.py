import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm


def test_user_id_is_incorrect(mock_login_service):
    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(
            username="wrong_id", password="test1234", scope=""
        )
        mock_login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_password_is_incorrect(mock_login_service):
    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(
            username="test_id", password="wrong_password1", scope=""
        )
        mock_login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_user_id_not_entered(mock_login_service):
    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(
            username="", password="password", scope=""
        )
        mock_login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_password_not_entered(mock_login_service):
    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(username="test_id", password="", scope="")
        mock_login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_user_id_and_password_not_enterd(mock_login_service):
    with pytest.raises(HTTPException) as response:
        form_data = OAuth2PasswordRequestForm(username="", password="", scope="")
        mock_login_service.login(form_data)

    assert response.value.status_code == 401
    assert response.value.detail == "아이디나 비밀번호가 틀렸습니다."


def test_login(mock_login_service):
    form_data = OAuth2PasswordRequestForm(
        username="test_id", password="test1234", scope=""
    )
    token = mock_login_service.login(form_data)

    assert type(token.access_token) == str
    assert token.token_type == "bearer"

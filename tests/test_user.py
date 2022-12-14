from fastapi.testclient import TestClient
from main import app
from core.config import settings

client = TestClient(app)

BASE_URL = f"{settings.API_V1_STR}"
ID = 0


def test_get_unknown_user():
    response = client.get(f"{BASE_URL}/user/999999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "사용자를 찾을 수 없습니다."}


def test_dont_match_password():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "test_user",
            "nickname": "test",
            "password": "testtest1",
            "password_check": "testtest2",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "비밀번호가 일치하지 않습니다."}


def test_short_password():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "test_user",
            "nickname": "test",
            "password": "1",
            "password_check": "1",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "비밀번호 길이가 너무 짧습니다."}


def test_without_lowercases_in_password():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "test_user",
            "nickname": "test",
            "password": "12345678",
            "password_check": "12345678",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "비밀번호는 한개 이상의 영소문자가 필수적으로 들어가야 합니다."}


def test_without_numbers_in_password():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "test_user",
            "nickname": "test_user",
            "password": "testwithoutnumber",
            "password_check": "testwithoutnumber",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "비밀번호는 한개 이상의 숫자가 필수적으로 들어가야 합니다."}


def test_max_length_in_userid():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "testuserhelloworld",
            "nickname": "test_user",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "user_id"]
    assert response.json()["detail"][0]["msg"] == "ensure this value has at most 15 characters"


def test_max_length_in_nickname():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "test_user",
            "nickname": "testuserhelloworld",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "nickname"]
    assert response.json()["detail"][0]["msg"] == "ensure this value has at most 15 characters"


def test_min_length_in_userid():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "",
            "nickname": "test_user",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "user_id"]
    assert response.json()["detail"][0]["msg"] == "ensure this value has at least 1 characters"


def test_min_length_in_nickname():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "test_user",
            "nickname": "",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "nickname"]
    assert response.json()["detail"][0]["msg"] == "ensure this value has at least 1 characters"


def test_userid_is_empty():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "nickname": "test_user",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "user_id"]
    assert response.json()["detail"][0]["msg"] == "field required"


def test_nickname_is_empty():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "test_user",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "nickname"]
    assert response.json()["detail"][0]["msg"] == "field required"


def test_create_user():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "test_user",
            "nickname": "test_user",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    global ID
    ID = response.json()['id']

    assert response.status_code == 201
    assert response.json() == {'id': ID, 'nickname': 'test_user'}


def test_create_existing_user():
    response = client.post(
        f"{BASE_URL}/user/",
        json={
            "user_id": "test_user",
            "nickname": "test_user",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "이미 존재하는 사용자입니다."}


def test_get_user():
    response = client.get(f"{BASE_URL}/user/{ID}/")
    assert response.status_code == 200
    assert response.json() == {'id': ID, 'nickname': 'test_user'}


def test_update_user():
    response = client.put(
        f"{BASE_URL}/user/{ID}/",
        json={
            "nickname": "amend_user",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 200
    assert response.json() == {'id': ID, 'nickname': 'amend_user'}


def test_delete_user():
    response = client.delete(
        f"{BASE_URL}/user/{ID}/"
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "탈퇴되었습니다."}



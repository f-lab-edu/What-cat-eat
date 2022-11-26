from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 에러가 있어서 수정 후 추가 예정
# def test_do_not_input_all_field():
#     response = client.post(
#         "/user/",
#         json={

#         }
#     )
#     assert response.status_code == 400
#     assert response.json() == {
#         "detail": "필드를 모두 채워주세요"
#     }


def test_get_unknown_user():
    response = client.get("/api/user/999999/")
    assert response.status_code == 404
    assert response.json() == {"detail": "사용자를 찾을 수 없습니다."}


def test_dont_match_password():
    response = client.post(
        "/api/user/",
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
        "/api/user/",
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
        "/api/user/",
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
        "/api/user/",
        json={
            "user_id": "test_user",
            "nickname": "test_user",
            "password": "testwithoutnumber",
            "password_check": "testwithoutnumber",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "비밀번호는 한개 이상의 숫자가 필수적으로 들어가야 합니다."}


def test_create_user():
    response = client.post(
        "/api/user/",
        json={
            "user_id": "test_user",
            "nickname": "test_user",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"detail": "사용자가 생성되었습니다."}


def test_create_existing_user():
    response = client.post(
        "/api/user/",
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
    response = client.get("/api/user/1/")
    assert response.status_code == 200
    assert response.json() == {"nickname": "test_user", "id": 1}


def test_update_user():
    response = client.put(
        "/api/user/1/",
        json={
            "nickname": "test_user_amend",
            "password": "testuser1",
            "password_check": "testuser1",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "수정되었습니다."}

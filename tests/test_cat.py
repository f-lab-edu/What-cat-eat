import pytest
from fastapi import HTTPException
from schema.cat import CatCreate, CatUpdate
from tests.conftest import MOCK_TEST_CAT, MOCK_TEST_USER, MOCK_TEST_USER_NEW
from datetime import datetime


def test_get_cat(mock_cat_service):
    cat = mock_cat_service.get(MOCK_TEST_CAT.id)
    assert cat.id == 1
    assert cat.name == "test_cat"


def test_get_unknown_cat(mock_cat_service):
    with pytest.raises(HTTPException) as response:
        mock_cat_service.get(999999)

    assert isinstance(response.value, HTTPException)
    assert response.value.status_code == 404
    assert response.value.detail == "해당 고양이를 찾을 수 없습니다."


def test_duplicate_represent_cat(mock_cat_service):
    with pytest.raises(HTTPException) as response:
        mock_cat_service.create(
            CatCreate(
                id=2,
                represent_cat=True,
                name="test_cat2",
                birth=datetime.now(),
                gender="Male",
                species="코리안 숏 헤어",
                weight=5,
            ),
            MOCK_TEST_USER.user_id,
        )
    assert isinstance(response.value, HTTPException)
    assert response.value.status_code == 409
    assert response.value.detail == "이미 대표 고양이가 있습니다."


def test_not_found_user(mock_cat_service):
    with pytest.raises(HTTPException) as response:
        mock_cat_service.create(
            CatCreate(
                id=2,
                represent_cat=False,
                name="test_cat2",
                birth=datetime.now(),
                gender="Male",
                species="코리안 숏 헤어",
                weight=5,
            ),
            "unknown_user",
        )
    assert isinstance(response.value, HTTPException)
    assert response.value.status_code == 404
    assert response.value.detail == "사용자를 찾을 수 없습니다."


def test_create_cat(mock_cat_service):
    cat = mock_cat_service.create(
        CatCreate(
            id=2,
            represent_cat=False,
            name="test_cat2",
            birth=datetime.now(),
            gender="Male",
            species="코리안 숏 헤어",
            weight=5,
        ),
        MOCK_TEST_USER.user_id,
    )
    assert cat.id == 2
    assert cat.name == "test_cat2"


def test_update_another_users_cat(mock_cat_service_new):
    with pytest.raises(HTTPException) as response:
        mock_cat_service_new.update(
            MOCK_TEST_CAT.id,
            CatUpdate(
                represent_cat=False,
                name="test_cat_amend",
                birth=datetime.now(),
                gender="Female",
                species="샴",
                weight=3,
            ),
            MOCK_TEST_USER_NEW.user_id,
        )

    assert response.value.status_code == 401
    assert response.value.detail == "user가 다릅니다. 권한이 없습니다."


def test_update_already_represent_cat(mock_cat_service):
    with pytest.raises(HTTPException) as response:
        mock_cat_service.update(
            MOCK_TEST_CAT.id,
            CatUpdate(
                represent_cat=True,
                name="test_cat_amend",
                birth=datetime.now(),
                gender="Female",
                species="샴",
                weight=3,
            ),
            MOCK_TEST_USER.user_id,
        )

    assert response.value.status_code == 409
    assert response.value.detail == "이미 대표 고양이가 있습니다."


def test_update_cat(mock_cat_service):
    amend_cat = mock_cat_service.update(
        MOCK_TEST_CAT.id,
        CatUpdate(
            represent_cat=False,
            name="test_cat_amend",
            birth=datetime.now(),
            gender="Female",
            species="샴",
            weight=3,
        ),
        MOCK_TEST_USER.user_id,
    )

    assert amend_cat.name == "test_cat_amend"
    assert amend_cat.species == "샴"


def test_delete_another_cat(mock_cat_service_new):
    with pytest.raises(HTTPException) as response:
        mock_cat_service_new.delete(MOCK_TEST_CAT.id, MOCK_TEST_USER_NEW.user_id)

    assert response.value.status_code == 401
    assert response.value.detail == "user가 다릅니다. 권한이 없습니다."


def test_delete_cat(mock_user_service):
    count = mock_user_service.delete(MOCK_TEST_CAT.id, MOCK_TEST_USER.user_id)

    assert count == 0

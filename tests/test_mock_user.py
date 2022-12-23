import pytest
from repositories.UserRepository import FakeRepository
from services.UserServices import UserService
from schema.user import UserGet
from models.user import User


@pytest.fixture
def user_service():
    repository = FakeRepository()
    return UserService(userRepository=repository)

# @pytest.fixture
def test_user_create(user_service):
    id = 1
    user_id = 'test_id'
    nickname = 'test_nickname'
    password = 'test1234'
    user = user_service.create(User(
        id = id,
        user_id = user_id,
        nickname = nickname,
        password = password
    ))

    assert user.id == 1
    return user


def test_get_user(user_service):
    user = test_user_create(user_service)
    user_get = user_service.get(id=user.id)

    assert user_get.id == 1
    assert user_get.user_id == 'test_id'


def test_update_user(user_service):
    user = test_user_create(user_service)
    user_update = user_service.update(user.id, User(
        nickname = 'amend_user',
        password = 'test1234'
    ))
    
    assert user_update.nickname == 'amend_user'

def test_delete_user(user_service):
    user = test_user_create(user_service)
    count = user_service.delete(user.id)

    assert count == 0
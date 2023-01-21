from datetime import datetime
import pytest
from passlib.context import CryptContext

from models.user import User
from repositories.UserRepository import FakeRepository
from services.LoginService import LoginService
from services.UserServices import UserService

MOCK_TEST_USER = User(
    id=1,
    user_id="test_id",
    password=CryptContext(schemes=["bcrypt"], deprecated="auto").hash("test1234"),
    nickname="test_nickname",
    created_at=datetime.now(),
    updated_at=datetime.now(),
)


def mock_fake_repository():
    repository = FakeRepository()
    repository.create(MOCK_TEST_USER)
    return repository


@pytest.fixture(autouse=True)
def mock_user_service():
    return UserService(userRepository=mock_fake_repository())


@pytest.fixture(autouse=True)
def mock_login_service():
    return LoginService(userRepository=mock_fake_repository())

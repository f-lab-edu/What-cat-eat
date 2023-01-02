from pydantic import BaseModel, Field
import re
from typing import Optional


class UserBase(BaseModel):
    id: Optional[int] = Field(primary_key=True)
    nickname: str = Field(min_length=1, max_length=15)
    password: str


class UserCreate(UserBase):
    user_id: str = Field(min_length=1, max_length=15)


class UserUpdate(UserBase):
    pass


class UserGet(BaseModel):
    id: int
    nickname: str

    class Config:
        orm_mode = True


class ValidatePassword(BaseModel):
    success: bool
    status_code: int = 200
    error: str = None


def validate_password(password) -> ValidatePassword:
    if len(password) < 8:
        return ValidatePassword(success=False, status_code=400, error="비밀번호가 너무 짧습니다.")

    if re.search(r"[a-z]", password) is None:
        return ValidatePassword(
            success=False, status_code=400, error="비밀번호는 한개 이상의 영소문자가 필수적으로 들어가야 합니다."
        )

    if re.search(r"\d", password) is None:
        return ValidatePassword(
            success=False, status_code=400, error="비밀번호는 한개 이상의 숫자가 필수적으로 들어가야 합니다."
        )

    return {"success": True}

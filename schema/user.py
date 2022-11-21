from pydantic import BaseModel, Field
from fastapi import HTTPException


class UserBase(BaseModel):
    nickname: str = Field(default=None, max_lenght=15)
    password: str
    password_check: str

    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("필드를 모두 채워주세요")
        return v

    def validate_password(cls, values):
        if values.password_check != values.password:
            raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
        return values.password


class UserCreate(UserBase):
    user_id: str = Field(default=None, max_lenght=15)


class UserUpdate(UserBase):
    pass

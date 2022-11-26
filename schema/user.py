from pydantic import BaseModel, Field
from fastapi import HTTPException
import re


class UserBase(BaseModel):
    nickname: str = Field(default=None, max_lenght=15)

    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("필드를 모두 채워주세요")
        return v

    def validate_password(cls, values):
        if values.password_check != values.password:
            raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")

        if len(values.password) < 8:
            raise HTTPException(status_code=400, detail="비밀번호 길이가 너무 짧습니다.")

        if re.search(r"[a-z]", values.password) is None:
            raise HTTPException(
                status_code=400, detail="비밀번호는 한개 이상의 영소문자가 필수적으로 들어가야 합니다."
            )
        if re.search(r"\d", values.password) is None:
            raise HTTPException(
                status_code=400, detail="비밀번호는 한개 이상의 숫자가 필수적으로 들어가야 합니다."
            )

        return values.password


class UserCreate(UserBase):
    user_id: str = Field(default=None, max_lenght=15)
    password: str
    password_check: str


class UserUpdate(UserBase):
    password: str
    password_check: str


class UserGet(UserBase):
    id: int

    class Config:
        orm_mode = True

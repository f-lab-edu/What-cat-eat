from pydantic import BaseModel, validator


class UserCreate(BaseModel):
    user_id: str
    password: str
    password_check: str
    nickname: str


    @validator('user_id', 'password', 'password_check', 'nickname')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('필드를 모두 채워주세요')
        return v

    @validator('password_check')
    def validate_password(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('비밀번호가 일치하지 않습니다.')

        return v
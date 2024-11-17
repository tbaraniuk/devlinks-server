import uuid
from pydantic import BaseModel, EmailStr, field_serializer
from typing import Optional

from .token import Token


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserGet(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    links: Optional[list] = None
    avatar_id: Optional[str] = None

    @field_serializer('id', when_used='json')
    def serialize_id(self, value: uuid.UUID) -> str:
        return str(value)


class UserSchema(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: bytes
    links: Optional[list] = None
    avatar_id: Optional[str] = None

    @field_serializer('id', when_used='json')
    def serialize_id(self, value: uuid.UUID) -> str:
        return str(value)


class RegisterGetUserSchema(BaseModel):
    user: UserGet
    token: Token

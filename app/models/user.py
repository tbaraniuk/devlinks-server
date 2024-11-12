import uuid

from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr

from models.link import Link


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(nullable=False, unique=True)
    first_name: str = Field(default=None, nullable=True)
    last_name: str = Field(default=None, nullable=True)
    email: EmailStr
    password: str

    links: list["Link"] = Relationship()
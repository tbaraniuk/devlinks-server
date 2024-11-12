import uuid

from sqlmodel import Field, SQLModel
from pydantic import HttpUrl


class Link(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    platform: str = Field(default=None)
    link: str = Field(default=None)

    owner_id: uuid.UUID = Field(foreign_key="user.id")
import uuid
from pydantic import BaseModel, field_serializer
from typing import Optional


class LinkSchema(BaseModel):
    id: Optional[uuid.UUID]
    platform: str
    link: str

    @field_serializer('id')
    def serialize_id(self, value: uuid.UUID) -> str:
        return str(value)


class LinkCreateSchema(BaseModel):
    platform: str
    link: str


class GetLinksSchema(BaseModel):
    links: list[LinkSchema]

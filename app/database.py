from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

from config import settings


engine = create_engine(settings.db.url, echo=settings.db.echo)


def create_db_and_tables():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

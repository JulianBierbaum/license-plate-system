from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import settings

engine = create_engine(str(settings.db_uri))


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a SQLAlchemy session.

    This function is a generator that yields a SQLAlchemy session object.
    It ensures that the session is properly closed after use.

    Yields:
        Session: A SQLAlchemy session object.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.db.session import get_db  # Assuming this is your dependency override point
from src.main import app

test_engine = create_engine(str(settings.db_uri))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db():
    """
    Provides a SQLAlchemy session for each test function.
    Each test will run within its own transaction, which is then rolled back
    at the end of the test, ensuring data isolation without dropping tables.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db):
    """
    Provides a FastAPI test client configured to use the `db` fixture's session.
    """

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        # Clear overrides to ensure subsequent tests don't use this override
        app.dependency_overrides.clear()

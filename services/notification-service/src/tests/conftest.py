import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import settings
from src.db.session import get_db
from src.main import app

test_engine = create_engine(str(settings.db_uri))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope='function')
def db():
    """
    Provides a SQLAlchemy session for each test function.
    Mocks session.commit() to be a flush() instead, so changes are visible
    within the transaction but not persisted.
    Rolls back the transaction at the end of the test.
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    session.commit = session.flush

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope='function')
def client(db):
    """
    Provides a FastAPI test client configured to use the `db` fixture's session.
    Auth is bypassed for testing by overriding the verify_api_key dependency.
    """
    from src.api.auth import verify_api_key

    def override_get_db():
        yield db

    async def override_verify_api_key():
        return 'test-api-key'

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[verify_api_key] = override_verify_api_key
    try:
        yield TestClient(app)
    finally:
        # Clear overrides to ensure subsequent tests don't use this override
        app.dependency_overrides.clear()


@pytest.fixture(scope='function')
def email_handler():
    """Create an EmailHandler with test config"""
    from src.handlers.email_handler import EmailHandler

    return EmailHandler(
        smtp_host='test.smtp.local',
        smtp_port=25,
        sender_address='test@example.com',
    )

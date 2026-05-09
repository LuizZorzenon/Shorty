import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app

from app.core.database import Base, get_db
from app.core.settings import settings

TEST_DATABASE_URL = settings.DATABASE_URL_TEST

engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()

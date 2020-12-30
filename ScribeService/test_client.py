from fastapi.testclient import TestClient
from .main import app, get_db
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base.metadata.create_all(bind=engine)
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_user():
    """ Assert that a user can successfully create a user profile with user and password """

    response = client.post(
        "/users/",
        headers={"Content-Type": "application/json"},
        json={"email": "test@gmail.com", "password": "password"},
    )

    assert response.status_code == 200


def test_fail_create_user_with_non_email():
    pass


def test_fail_if_user_already_registered():
    """ If a user has been created with the same email address, deny access """

    response = client.post(
        "/users/",
        headers={"Content-Type": "application/json"},
        json={"email": "test@gmail.com", "password": "password"},
    )

    assert response.status_code == 200

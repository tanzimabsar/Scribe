from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from ..database import Base
from ..main import app, get_db

# Flush the tsting database
db_file = 'test.db'

if os.path.isfile(db_file):
        os.remove(db_file)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_user():
    """ Assert that a user can successfully create a user profile with user and password """

    response = client.post(
        "/users",
        headers={"Content-Type": "application/json"},
        json={
            "email": "test@gmail.com", 
            "password": "password"
        },
    )

    assert response.status_code == 200

def test_fail_if_user_is_already_created():
    """ Assert that a user can successfully create a user profile with user and password """

    response = client.post(
        "/users",
        headers={"Content-Type": "application/json"},
        json={
            "email": "test@gmail.com", 
            "password": "password"
        },
    )

    assert response.status_code == 400

def test_get_token():


    response = client.post(
        "/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        json={
            "username": "test_user", 
            "password": "test"
        }
    )

    assert response.status_code == 200


from fastapi.testclient import TestClient
from .main import app


client = TestClient(app)

def test_get_users():
    """ Assert that a user can successfully create a user profile with user and password """

    response = client.post(
        "/users/",
        headers={'Content-Type': 'application/json'},
        json={"email": "test@gmail.com", "password": "password"},
    )

    assert response.status_code == 200
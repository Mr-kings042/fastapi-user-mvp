from fastapi.testclient import TestClient
from main import app



client = TestClient(app)


def test_create_user():
    payload = {
        "username": "testuser",
        "email": "test_user@gmail.com",
        "full_name": "Test User",
        "password": "testpassword123"
         }
    response = client.post("/user", json=payload)
    assert response.status_code == 201

    assert response.json()["message"] == "User created successfully"
    assert response.json()["has_error"] is False
    assert response.json()["data"]["username"] == "testuser"

#test for failed user creation due to existing username
def test_create_user_with_existing_username():
    payload = {
        "username": "testuser",
        "email": "kings@gmail.com",
        "full_name": "Test User",
        "password": "testpassword123"
    }
    client.post("/user", json=payload)
    duplicate_payload = {
        "username": "testuser",
        "email": "dejed@ham.com",
        "full_name": "Test User",
        "password": "testpasswofrd123"
    }
    response = client.post("/user", json=duplicate_payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Username already exists"
#test for failed user creation due to existing email
def test_create_user_with_existing_email():
    payload = {
        "username": "newuser",
        "email": "mailmail@mail.com",
        "full_name": "New User",
        "password": "newpassword123"
    }
    client.post("/user", json=payload)
    duplicate_payload = {
        "username": "anotheruser",
        "email": "mailmail@mail.com",
        "full_name": "Another User",
        "password": "anotherpassword123"
    }
    response = client.post("/user", json=duplicate_payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"
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

#Test for user login
def test_login_user():
    payload = {
        "username": "testuser",
        "password": "testpassword123"
    }
    response = client.post("/user/login", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"

def test_login_user_with_invalid_credentials():
    payload = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/user/login", json=payload)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or Password"


def test_get_all_users():
    response = client.get("/user/Users")
    assert response.status_code == 200
    assert response.json()["message"] == "Users retrieved successfully"
    assert isinstance(response.json()["data"], list)
    assert response.json()["has_error"] is False

def update_user():
    payload = {
        "username": "updateduser",
        "email": "updatedmail@mail.com",
        "full_name": "Updated User",
        "password": "updatedpassword123"
    }
    response = client.put("/user/1", json=payload)
    assert response.status_code == 200
    assert response.json()["message"] == "User updated successfully"
    assert response.json()["data"]["username"] == "updateduser"
    assert response.json()["data"]["email"] == "updatedmail@mail.com"
def test_update_user_with_non_existent_id():
    payload = {
        "username": "nonexistentuser",
        "email": "jdwiduu@uddmail.com",
        "full_name": "Non Existent User",
        "password": "nonexistentpassword123"
    }
    response = client.put("/user/1000", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_user_by_id():
    response = client.get("/user/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User retrieved successfully"
    assert response.json()["data"]["id"] == 1
    assert response.json()["has_error"] is False
    
def test_get_user_by_non_existent_id():
    response = client.get("/user/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user():
    response = client.delete("/user/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
    assert response.json()["has_error"] is False
def test_delete_non_existent_user():
    response = client.delete("/user/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
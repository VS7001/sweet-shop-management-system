from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_registration():
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_duplicate_user_registration():
    client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"

def test_user_login_success():
    # register user first
    client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    # login with same credentials
    response = client.post(
        "/api/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_returns_token():
    client.post(
        "/api/auth/register",
        json={
            "email": "jwt@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": "jwt@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_success():
    response = client.post(
        "/register",
        json={
            "username": "alice_day2",
            "password": "123456"
        }
    )

    assert response.status_code == 201

    assert response.json() == {
        "message": "User registered successfully",
        "username": "alice_day2"
    }

    assert "password" not in response.json()


def test_register_duplicate_username():
    user_data = {
        "username": "duplicate_user",
        "password": "123456"
    }

    first_response = client.post(
        "/register",
        json=user_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/register",
        json=user_data
    )

    assert second_response.status_code == 400

    assert second_response.json() == {
        "detail": "Username already exists"
    }


def test_register_empty_username():
    response = client.post(
        "/register",
        json={
            "username": "",
            "password": "123456"
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Username cannot be empty"
    }


def test_register_empty_password():
    response = client.post(
        "/register",
        json={
            "username": "empty_password_user",
            "password": ""
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Password cannot be empty"
    }


def test_register_whitespace_username():
    response = client.post(
        "/register",
        json={
            "username": "   ",
            "password": "123456"
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Username cannot be empty"
    }


def test_register_missing_password():
    response = client.post(
        "/register",
        json={
            "username": "missing_password_user"
        }
    )

    assert response.status_code == 422
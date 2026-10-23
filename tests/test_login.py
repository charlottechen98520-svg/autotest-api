from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def register_test_user(username, password="123456"):
    response = client.post(
        "/register",
        json={
            "username": username,
            "password": password
        }
    )

    assert response.status_code == 201


def test_login_success():
    register_test_user(
        "login_success_user",
        "123456"
    )

    response = client.post(
        "/login",
        json={
            "username": "login_success_user",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Login successful",
        "username": "login_success_user"
    }

    assert "password" not in response.json()


def test_login_wrong_password():
    register_test_user(
        "wrong_password_user",
        "123456"
    )

    response = client.post(
        "/login",
        json={
            "username": "wrong_password_user",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid username or password"
    }


def test_login_unknown_username():
    response = client.post(
        "/login",
        json={
            "username": "user_that_does_not_exist",
            "password": "123456"
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid username or password"
    }


def test_login_empty_username():
    response = client.post(
        "/login",
        json={
            "username": "",
            "password": "123456"
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Username cannot be empty"
    }


def test_login_empty_password():
    response = client.post(
        "/login",
        json={
            "username": "empty_password_login_user",
            "password": ""
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Password cannot be empty"
    }


def test_login_whitespace_username():
    response = client.post(
        "/login",
        json={
            "username": "   ",
            "password": "123456"
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Username cannot be empty"
    }


def test_login_missing_password():
    response = client.post(
        "/login",
        json={
            "username": "missing_password_login_user"
        }
    )

    assert response.status_code == 422
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_task_success():
    response = client.post(
        "/tasks",
        json={
            "title": "Day 4 test task",
            "description": "Learn POST tasks"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Day 4 test task"
    assert data["description"] == "Learn POST tasks"
    assert data["completed"] is False

    assert "id" in data
    assert isinstance(data["id"], int)

def test_create_task_without_description():
    response = client.post(
        "/tasks",
        json={
            "title": "Task without description"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == "Task without description"
    assert data["description"] == ""
    assert data["completed"] is False

def test_create_task_empty_title():
    response = client.post(
        "/tasks",
        json={
            "title": "",
            "description": "Invalid task"
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Task title cannot be empty"
    }

def test_create_task_whitespace_title():
    response = client.post(
        "/tasks",
        json={
            "title": "    ",
            "description": "Invalid task"
        }
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Task title cannot be empty"
    }

def test_create_task_missing_title():
    response = client.post(
        "/tasks",
        json={
            "description": "Missing title"
        }
    )

    assert response.status_code == 422

def test_get_tasks():
    client.post(
        "/tasks",
        json={
            "title": "Task for GET test",
            "description": "Check GET /tasks"
        }
    )

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert any(
        task["title"] == "Task for GET test"
        for task in data
    )
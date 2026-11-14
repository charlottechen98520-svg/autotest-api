from fastapi.testclient import TestClient
from app.main import app

import pytest

client = TestClient(app)

def create_test_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Day 5 Test Task",
            "description": "Testing CRUD operations"
        }
    )

    assert response.status_code == 201

    return response.json()["id"]

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

def test_get_task_by_id_success():
    task_id = create_test_task()

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Day 5 Test Task"
    assert data["completed"] is False


def test_get_task_not_found():
    response = client.get("/tasks/-1")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_get_task_invalid_id():
    response = client.get("/tasks/abc")

    assert response.status_code == 422

def test_update_task_success():
    task_id = create_test_task()

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "description": "Updated Description",
            "completed": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["completed"] is True

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 200
    assert get_response.json() == data


def test_update_task_not_found():
    response = client.put(
        "/tasks/-1",
        json={
            "title": "Updated Task",
            "description": "Test",
            "completed": True
        }
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }


def test_update_task_empty_title():
    task_id = create_test_task()

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "",
            "description": "Invalid Update",
            "completed": True
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Task title cannot be empty"
    }

def test_delete_task_success():
    task_id = create_test_task()

    delete_response = client.delete(
        f"/tasks/{task_id}"
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(
        f"/tasks/{task_id}"
    )

    assert get_response.status_code == 404


def test_delete_task_not_found():
    response = client.delete("/tasks/-1")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found"
    }

def test_tasks_start_empty(api_client):
    response = api_client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.parametrize(
    "payload,expected_status",
    [
        (
            {"title": "", "description": "Test"},
            400
        ),
        (
            {"title": "   ", "description": "Test"},
            400
        ),
        (
            {"description": "Missing title"},
            422
        ),
        (
            {"title": "Valid title", "description": None},
            422
        )
    ],
    ids=[
        "empty-title",
        "whitespace-title",
        "missing-title",
        "invalid-description-type"
    ]
)
def test_create_task_invalid_inputs(
    api_client,
    payload,
    expected_status
):
    response = api_client.post(
        "/tasks",
        json=payload
    )

    assert response.status_code == expected_status
import pytest

from fastapi.testclient import TestClient
from app import main as main_module


@pytest.fixture(autouse=True)
def reset_test_data():
    main_module.users.clear()
    main_module.tasks.clear()
    main_module.next_task_id = 1

    yield

    main_module.users.clear()
    main_module.tasks.clear()
    main_module.next_task_id = 1


@pytest.fixture
def api_client():
    return TestClient(main_module.app)
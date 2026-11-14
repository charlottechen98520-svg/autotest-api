import os

os.environ["DB_NAME"] = "autotest_test"

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_connection


def clear_test_database():
    with get_connection() as conn:
        with conn.cursor() as cursor:

            cursor.execute(
                "SELECT DATABASE() AS db_name"
            )

            database_name = cursor.fetchone()["db_name"]

            if database_name != "autotest_test":
                raise RuntimeError(
                    "Refusing to clean a non-test database"
                )

            cursor.execute("DELETE FROM tasks")
            cursor.execute("DELETE FROM users")

            conn.commit()


@pytest.fixture(autouse=True)
def reset_test_data():
    clear_test_database()

    yield

    clear_test_database()


@pytest.fixture
def api_client():
    return TestClient(app)
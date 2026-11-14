import os

import pymysql
from dotenv import load_dotenv


load_dotenv()


def get_connection():
    db_name = os.getenv("DB_NAME")

    if db_name not in ("autotest_dev", "autotest_test"):
        raise RuntimeError("Invalid database name")

    password = os.getenv("DB_PASSWORD")
    if password is None:
        raise RuntimeError("DB_PASSWORD is not configured")

    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "autotest_app"),
        password=password,
        database=db_name,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )
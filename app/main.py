import pymysql

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from pwdlib import PasswordHash

from app.database import get_connection

app = FastAPI()

password_hash = PasswordHash.recommended()


class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str = ""

class TaskUpdate(BaseModel):
    title: str
    description: str
    completed: bool

def to_task(row):
    return {
        "id": row["id"],
        "title": row["title"],
        "description": row["description"],
        "completed": bool(row["completed"])
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    username = user.username.strip()
    password = user.password.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty"
        )

    if not password:
        raise HTTPException(
            status_code=400,
            detail="Password cannot be empty"
        )

    hashed_password = password_hash.hash(password)

    with get_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    """
                    INSERT INTO users (username, password_hash)
                    VALUES (%s, %s)
                    """,
                    (username, hashed_password)
                )

                conn.commit()

            except pymysql.err.IntegrityError:
                conn.rollback()

                raise HTTPException(
                    status_code=400,
                    detail="Username already exists"
                )

    return {
        "message": "User registered successfully",
        "username": username
    }

@app.post("/login")
def login_user(user: UserLogin):
    username = user.username.strip()
    password = user.password.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username cannot be empty"
        )

    if not password:
        raise HTTPException(
            status_code=400,
            detail="Password cannot be empty"
        )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT username, password_hash
                FROM users
                WHERE username = %s
                """,
                (username,)
            )

            existing_user = cursor.fetchone()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not password_hash.verify(
        password,
        existing_user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "message": "Login successful",
        "username": existing_user["username"]
    }


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    title = task.title.strip()
    description = task.description.strip()

    if not title:
        raise HTTPException(
            status_code=400,
            detail="Task title cannot be empty"
        )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks
                    (title, description, completed)
                VALUES (%s, %s, %s)
                """,
                (title, description, False)
            )

            task_id = cursor.lastrowid
            conn.commit()

    return {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False
    }

@app.get("/tasks")
def get_tasks():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, description, completed
                FROM tasks
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

    return [to_task(row) for row in rows]



@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, title, description, completed
                FROM tasks
                WHERE id = %s
                """,
                (task_id,)
            )

            row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return to_task(row)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    title = update.title.strip()

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM tasks
                WHERE id = %s
                """,
                (task_id,)
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )

            if not title:
                raise HTTPException(
                    status_code=400,
                    detail="Task title cannot be empty"
                )

            description = update.description.strip()

            cursor.execute(
                """
                UPDATE tasks
                SET title = %s,
                    description = %s,
                    completed = %s
                WHERE id = %s
                """,
                (
                    title,
                    description,
                    update.completed,
                    task_id
                )
            )

            conn.commit()

    return {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": update.completed
    }

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                DELETE FROM tasks
                WHERE id = %s
                """,
                (task_id,)
            )

            if cursor.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )

            conn.commit()

    return Response(status_code=204)
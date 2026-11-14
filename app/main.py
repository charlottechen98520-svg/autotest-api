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

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    global next_task_id

    title = task.title.strip()
    description = task.description.strip()

    if title == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty"
        )

    new_task = {
        "id": next_task_id,
        "title": title,
        "description": description,
        "completed": False
    }

    tasks.append(new_task)

    next_task_id += 1

    return new_task

@app.get("/tasks")
def get_tasks():
    return tasks

def find_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task

    return None

@app.get("/tasks/{task_id}")
def get_task_by_id(task_id: int):
    task = find_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    task = find_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    title = update.title.strip()

    if title == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty"
        )

    task["title"] = title
    task["description"] = update.description.strip()
    task["completed"] = update.completed

    return task

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(task_id: int):
    task = find_task(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    tasks.remove(task)
    return None
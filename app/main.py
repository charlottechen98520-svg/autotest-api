from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


users = []
tasks = []

next_task_id = 1


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

    if username == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username cannot be empty"
        )

    if password == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be empty"
        )

    for existing_user in users:
        if existing_user["username"] == username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )

    users.append({
        "username": username,
        "password": password
    })

    return {
        "message": "User registered successfully",
        "username": username
    }



@app.post("/login")
def login_user(user: UserLogin):
    username = user.username.strip()
    password = user.password.strip()

    if username == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username cannot be empty"
        )

    if password == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password cannot be empty"
        )

    for existing_user in users:
        if existing_user["username"] == username:
            if existing_user["password"] != password:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password"
                )

            return {
                "message": "Login successful",
                "username": username
            }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )

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
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



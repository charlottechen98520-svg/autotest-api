from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI()


users = []


class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str


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
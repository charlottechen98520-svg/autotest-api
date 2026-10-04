# AutoTest API

A simple RESTful API project for learning automated API testing with FastAPI and pytest.

## Project Goal

The goal of this project is to build a small task management backend and create an automated testing framework for it.

This project is mainly used to practice:

- Python
- FastAPI
- RESTful API
- pytest
- Automated API Testing
- Git and GitHub

## Current Progress

- [x] Project repository created
- [x] Python virtual environment created
- [x] FastAPI installed
- [x] pytest installed
- [x] Added `GET /health` endpoint
- [x] Added automated test for `/health`
- [x] Test successfully passed
- [ ] User registration
- [ ] User login
- [ ] Task CRUD APIs
- [ ] MySQL database
- [ ] Database validation
- [ ] GitHub Actions CI
- [ ] Performance testing

## Project Structure

autotest-api/
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_health.py
├── .gitignore
├── requirements.txt
└── README.md

## Run the Server

First activate the virtual environment.
On macOS:
source .venv/bin/activate
Then start the FastAPI server:
fastapi dev app/main.py
Open in browser:
http://127.0.0.1:8000/health
Expected response:
{
  "status": "ok"
}
FastAPI API documentation:
http://127.0.0.1:8000/docs

## Run Tests

run:
python -m pytest -q
Current expected result:
1 passed

## Team

This project is developed by two Computer Science students as a learning project for software testing and test development.


# AutoTest — RESTful API Automated Testing Project

A lightweight RESTful API service and automated testing project built with **Python, FastAPI, and pytest**.

---

## 1. Project Overview

AutoTest is a collaborative software development and quality assurance project designed to explore backend development, RESTful API testing, automated test execution, and software testing practices.

The project consists of two major components:

1. **Backend Service:** A lightweight task management service providing user registration, login, and task management APIs.
2. **Automated Testing:** A pytest-based testing suite that validates API functionality, response status codes, input validation, and error handling.

The long-term goal is to develop a maintainable automated API testing framework integrated with database validation, continuous integration, test reporting, and AI-assisted test analysis.

### Project Objectives

- Develop RESTful APIs using FastAPI.
- Design functional, negative, and boundary test cases.
- Implement automated API tests using pytest.
- Validate HTTP status codes and JSON responses.
- Practice collaborative development using Git and GitHub.
- Improve test reliability, maintainability, and code quality.
- Integrate database verification, CI/CD, and performance testing in later stages.
- Explore AI-assisted test case generation and failure analysis in later stages.

---

## 2. Technology Stack

| Category | Technology | Purpose |
|---|---|---|
| Programming Language | Python | Backend and automated test development |
| Backend Framework | FastAPI | RESTful API development |
| Data Validation | Pydantic | Request body validation |
| Testing Framework | pytest | Automated test execution |
| API Test Client | FastAPI TestClient | Sending test requests and verifying responses |
| Development Tools | VS Code | Code development |
| Version Control | Git | Source code management |
| Collaboration | GitHub | Repository management, pull requests, and code reviews |
| Database (Planned) | MySQL | Persistent storage and database validation |
| Continuous Integration (Planned) | GitHub Actions | Automated regression testing |
| Performance Testing (Planned) | Locust | API performance evaluation |
| AI Integration (Planned) | LLM API | Test generation and failure analysis |

---

## 3. Project Architecture

```text
              Client / API Test Client
                        |
                        | HTTP Requests
                        v
                 FastAPI Backend
                        |
                Request Validation
                        |
                 Business Logic
                        |
            +-----------+-----------+
            |                       |
            v                       v
      In-Memory Users         In-Memory Tasks
        (Temporary)             (Temporary)


              Automated Test Suite
                        |
                        v
                  pytest Tests
                        |
              +---------+---------+
              |                   |
              v                   v
         HTTP Status         JSON Response
         Validation           Validation
              |                   |
              +---------+---------+
                        |
                        v
                    PASS / FAIL
```

**Current Implementation:** User and task information are temporarily stored in memory using Python lists.

**Future Implementation:** MySQL will replace in-memory storage and support database-level test validation.

---

## 4. Project Structure

```text
autotest-api/
|
|-- app/
|   |-- __init__.py
|   |-- main.py
|
|-- tests/
|   |-- test_health.py
|   |-- test_register.py
|   |-- test_login.py
|   |-- test_tasks.py
|
|-- .gitignore
|-- requirements.txt
|-- README.md
```

### File Descriptions

| File | Description |
|---|---|
| `app/main.py` | FastAPI application and API endpoint implementations |
| `app/__init__.py` | Python package initialization |
| `tests/test_health.py` | Health check automated tests |
| `tests/test_register.py` | User registration automated tests |
| `tests/test_login.py` | User login automated tests |
| `tests/test_tasks.py` | Task creation and retrieval automated tests |
| `.gitignore` | Excludes virtual environments and temporary files |
| `requirements.txt` | Python package dependencies |
| `README.md` | Project documentation |

The project structure will be extended as additional APIs and automated testing features are implemented.

---

## 5. Installation and Setup

### Prerequisites

Ensure the following tools are installed:

- Python 3.11 or later
- Git
- VS Code or another code editor

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/autotest-api.git
```

Replace `YOUR_USERNAME` with the actual GitHub repository owner.

Navigate into the project directory:

```bash
cd autotest-api
```

### Step 2: Create a Virtual Environment

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Start the FastAPI Server

```bash
fastapi dev app/main.py
```

The local development server should be accessible at:

```text
http://127.0.0.1:8000
```

### Step 5: Access Interactive API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically generates interactive API documentation that can be used to inspect and manually test available endpoints.

---

## 6. Implemented RESTful APIs

The following endpoints are currently implemented.

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/health` | Check API service availability | 200 |
| POST | `/register` | Register a new user | 201 |
| POST | `/login` | Login using username and password | 200 |
| POST | `/tasks` | Create a new task | 201 |
| GET | `/tasks` | Retrieve all tasks | 200 |

---

### 6.1 Health Check API

**Endpoint:**

```http
GET /health
```

**Expected Response:**

Status: `200 OK`

```json
{
  "status": "ok"
}
```

This endpoint verifies that the FastAPI application is running and responding to requests.

---

### 6.2 User Registration API

**Endpoint:**

```http
POST /register
```

**Request Body:**

```json
{
  "username": "alice",
  "password": "123456"
}
```

**Successful Response:**

Status: `201 Created`

```json
{
  "message": "User registered successfully",
  "username": "alice"
}
```

**Duplicate Username:**

Status: `400 Bad Request`

```json
{
  "detail": "Username already exists"
}
```

**Empty Username:**

Status: `400 Bad Request`

```json
{
  "detail": "Username cannot be empty"
}
```

**Empty Password:**

Status: `400 Bad Request`

```json
{
  "detail": "Password cannot be empty"
}
```

**Missing Required Field:**

Status: `422 Unprocessable Content`

FastAPI automatically performs request validation using Pydantic.

Example:

```json
{
  "username": "alice"
}
```

A request without the required `password` field results in a validation error.

### Current Registration Rules

- Username is required.
- Password is required.
- Empty usernames are rejected.
- Whitespace-only usernames are rejected.
- Empty passwords are rejected.
- Duplicate usernames are rejected.
- Leading and trailing whitespace is removed from usernames.
- Successful registration responses do not include the password.

---

### 6.3 User Login API

**Endpoint:**

```http
POST /login
```

**Request Body:**

```json
{
  "username": "alice",
  "password": "123456"
}
```

**Successful Response:**

Status: `200 OK`

```json
{
  "message": "Login successful",
  "username": "alice"
}
```

**Invalid Username or Password:**

Status: `401 Unauthorized`

```json
{
  "detail": "Invalid username or password"
}
```

The same error message is returned for an unknown username and an incorrect password.

This prevents the API from revealing whether a particular username exists.

**Empty Username:**

Status: `400 Bad Request`

```json
{
  "detail": "Username cannot be empty"
}
```

**Empty Password:**

Status: `400 Bad Request`

```json
{
  "detail": "Password cannot be empty"
}
```

**Missing Required Field:**

Status: `422 Unprocessable Content`

### Current Login Rules

- Username is required.
- Password is required.
- Empty usernames are rejected.
- Empty passwords are rejected.
- Whitespace-only usernames are rejected.
- Invalid credentials return `401 Unauthorized`.
- Passwords are never returned in API responses.

---

### 6.4 Create Task API

**Endpoint:**

```http
POST /tasks
```

**Request Body:**

```json
{
  "title": "Study Python",
  "description": "Complete Day 4 project"
}
```

**Successful Response:**

Status: `201 Created`

```json
{
  "id": 1,
  "title": "Study Python",
  "description": "Complete Day 4 project",
  "completed": false
}
```

The task ID is automatically generated by the backend.

The `completed` field is set to `false` when a new task is created.

The `description` field is optional.

Example:

```json
{
  "title": "Review DSA"
}
```

Possible response:

```json
{
  "id": 2,
  "title": "Review DSA",
  "description": "",
  "completed": false
}
```

**Empty Task Title:**

Status: `400 Bad Request`

```json
{
  "detail": "Task title cannot be empty"
}
```

**Missing Task Title:**

Status: `422 Unprocessable Content`

### Current Task Creation Rules

- Task title is required.
- Task description is optional.
- Empty task titles are rejected.
- Whitespace-only task titles are rejected.
- Task IDs are generated automatically.
- New tasks are marked as incomplete by default.

---

### 6.5 Get All Tasks API

**Endpoint:**

```http
GET /tasks
```

**Successful Response:**

Status: `200 OK`

Example:

```json
[
  {
    "id": 1,
    "title": "Study Python",
    "description": "Complete Day 4 project",
    "completed": false
  },
  {
    "id": 2,
    "title": "Review DSA",
    "description": "",
    "completed": false
  }
]
```

The API returns a list containing all currently stored tasks.

---

## 7. Automated API Testing

Automated tests are implemented using **pytest** and **FastAPI TestClient**.

The tests verify API behavior by comparing actual responses with predefined expected results.

### Testing Workflow

```text
Define API Requirement
        |
        v
Design Test Cases
        |
        v
Send HTTP Request
        |
        v
Receive API Response
        |
        v
Verify HTTP Status
        |
        v
Verify Response Body
        |
        v
     PASS / FAIL
```

---

### 7.1 Health Check Test

File:

```text
tests/test_health.py
```

The health test validates:

- The health endpoint is accessible.
- HTTP status code is `200`.
- The response contains the expected JSON data.

---

### 7.2 Registration API Tests

File:

```text
tests/test_register.py
```

| Test ID | Test Scenario | Expected Status |
|---|---|---|
| TC001 | Register with valid username and password | 201 |
| TC002 | Register with an existing username | 400 |
| TC003 | Register with an empty username | 400 |
| TC004 | Register with an empty password | 400 |
| TC005 | Register with whitespace-only username | 400 |
| TC006 | Register without a password field | 422 |

The successful registration test also verifies that passwords are not included in API responses.

---

### 7.3 Login API Tests

File:

```text
tests/test_login.py
```

| Test ID | Test Scenario | Expected Status |
|---|---|---|
| LOGIN01 | Login with valid username and password | 200 |
| LOGIN02 | Login with an incorrect password | 401 |
| LOGIN03 | Login with an unknown username | 401 |
| LOGIN04 | Login with an empty username | 400 |
| LOGIN05 | Login with an empty password | 400 |
| LOGIN06 | Login with whitespace-only username | 400 |
| LOGIN07 | Login without a password field | 422 |

Login tests introduce the concept of **test setup**.

A valid user must first be registered before a successful login can be tested.

A reusable helper function is used to prepare login test users.

Example workflow:

```text
Register Test User
        |
        v
POST /login
        |
        v
Validate Response
        |
        v
   PASS / FAIL
```

---

### 7.4 Task API Tests

File:

```text
tests/test_tasks.py
```

| Test ID | Test Scenario | Expected Status |
|---|---|---|
| TASK01 | Create a valid task | 201 |
| TASK02 | Create a task without description | 201 |
| TASK03 | Create a task with empty title | 400 |
| TASK04 | Create a task with whitespace-only title | 400 |
| TASK05 | Create a task without title field | 422 |
| TASK06 | Retrieve all tasks | 200 |

Task tests verify:

- Task creation.
- Automatically generated task IDs.
- Default task completion state.
- Optional descriptions.
- Input validation.
- Retrieval of task collections.

Task IDs are validated by checking that an `id` field exists and that its value is an integer rather than assuming a fixed task ID.

The GET task test verifies that the created task exists in the returned task list.

---

### 7.5 Running Automated Tests

Run:

```bash
python -m pytest -q
```

Current expected result:

```text
20 passed
```

Current automated test suite:

```text
Health tests:       1
Registration tests: 6
Login tests:        7
Task tests:         6
----------------------
Total:             20
```

The passing result should be confirmed locally before a project milestone is marked complete.

---

### 7.6 Example Test Failure

Suppose a test expects:

```text
Expected HTTP Status: 201
```

but the server returns:

```text
Actual HTTP Status: 404
```

pytest reports a failure.

This allows developers to identify missing functionality or behavior that does not match the agreed API specification.

Expected results should not be changed simply to make tests pass.

Instead, the implementation should be checked against the agreed requirements.

---

## 8. Testing Strategy

The project follows a lightweight test-first development approach.

### Functional Testing

Verify that valid requests produce the expected results.

Examples:

- A new user can register successfully.
- A registered user can login successfully.
- A valid task can be created.
- Existing tasks can be retrieved.

### Negative Testing

Verify that invalid requests are rejected.

Examples:

- Duplicate username.
- Incorrect password.
- Unknown username.
- Empty password.
- Empty task title.
- Missing required field.

### Boundary Testing

Verify behavior around special or edge input values.

Current examples:

- Whitespace-only usernames.
- Whitespace-only task titles.

Future scenarios may include:

- Maximum username length.
- Minimum password length.
- Maximum task title length.
- Oversized request bodies.
- Invalid data types.

### Regression Testing

Previously implemented tests are executed after every new feature to ensure existing functionality still works.

For example:

```text
Day 4 changes
    |
    v
Run all Health + Register + Login + Task tests
    |
    v
20 passed
```

---

## 9. Development Workflow

The project uses Git and GitHub for collaborative development.

```text
Requirements
    |
    v
API Contract
    |
    v
Test Case Design
    |
    v
Create Feature Branch
    |
    v
Write Automated Tests
    |
    v
Tests Initially FAIL
    |
    v
Implement Backend
    |
    v
Execute pytest
    |
    +---- FAIL ----> Debug and Fix
    |                    |
    |<-------------------+
    |
   PASS
    |
    v
Git Commit
    |
    v
Push Feature Branch
    |
    v
Pull Request
    |
    v
Peer Code Review
    |
    v
Merge into main
```

### Basic Git Commands

Create a feature branch:

```bash
git checkout -b feature/example-feature
```

Check changes:

```bash
git status
```

Stage files:

```bash
git add .
```

Commit:

```bash
git commit -m "describe the implemented feature"
```

Push:

```bash
git push -u origin feature/example-feature
```

After review and merge:

```bash
git checkout main
git pull origin main
```

Run regression tests:

```bash
python -m pytest -q
```

The `main` branch should remain in a working and tested state.

---

## 10. Team Collaboration

This project is developed by a two-person team.

Both members contribute to backend development, automated testing, debugging, Git workflows, and code review.

### Primary Responsibilities

| Role | Primary Focus | Secondary Focus |
|---|---|---|
| Member A | Automated testing and test design | Backend development |
| Member B | Backend and API implementation | Automated testing |

Responsibilities are rotated across features so that both members gain practical experience with the complete development and testing workflow.

---

### Day 1 Responsibilities

| Member A | Member B |
|---|---|
| Project initialization | pytest setup |
| FastAPI health endpoint | Health endpoint test |
| Branch and PR workflow | Test execution and review |

---

### Day 2 Responsibilities

| Member A | Member B |
|---|---|
| Registration API test design | Registration API implementation |
| Registration automated tests | Request validation and error handling |
| Test execution and verification | Backend debugging |
| Backend code review | Test code review |

---

### Day 3 Responsibilities

Roles were rotated.

| Member A | Member B |
|---|---|
| Login API implementation | Login test case design |
| Credential validation | Login automated tests |
| Backend debugging | Test setup and verification |
| Test code review | Backend code review |

Day 3 introduced test setup because a registered user is required before successful login can be tested.

---

### Day 4 Responsibilities

Roles were rotated again.

| Member A | Member B |
|---|---|
| Task API test design | Task API implementation |
| Task automated tests | Task storage and ID generation |
| Test result verification | Input validation |
| Backend code review | Test code review |

Day 4 introduced task creation and retrieval, shared in-memory task storage, automatic task IDs, and list response validation.

---

### Collaboration Principles

- Use a shared GitHub repository.
- Create branches for new features.
- Define API requirements before implementation.
- Design test cases before finalizing backend behavior.
- Run regression tests after every change.
- Review code before merging into `main`.
- Keep `main` functional.
- Ensure both members understand major technical decisions.
- Rotate development and testing responsibilities.

---

## 11. Development Progress

### Day 1 — Project Initialization

**Milestone: Project Bootstrap**

- [x] Create GitHub repository
- [x] Configure local development environments
- [x] Create Python virtual environments
- [x] Install FastAPI and pytest
- [x] Establish project directory structure
- [x] Implement `GET /health`
- [x] Create the first automated test
- [x] Verify successful test execution
- [x] Practice Git branching and commits
- [x] Create and review a pull request
- [x] Merge changes into `main`

**Milestone Result:** 1 passing automated test.

---

### Day 2 — User Registration

**Milestone: Registration API and Automated Tests**

- [x] Define registration API requirements
- [x] Design six registration test cases
- [x] Implement `POST /register`
- [x] Add Pydantic request validation
- [x] Implement duplicate username detection
- [x] Validate empty and invalid input
- [x] Add automated registration tests
- [x] Check successful and error responses
- [x] Review and integrate changes

**Milestone Result:** 7 passing automated tests.

---

### Day 3 — User Login

**Milestone: Login API and Automated Tests**

- [x] Define login API requirements
- [x] Design seven login test cases
- [x] Implement `POST /login`
- [x] Add login request model
- [x] Validate username and password
- [x] Handle incorrect credentials with `401 Unauthorized`
- [x] Add login test setup
- [x] Add automated login tests
- [x] Validate empty and missing inputs
- [x] Update API documentation
- [x] Review and merge changes

**Milestone Result:** 14 passing automated tests.

---

### Day 4 — Task Creation and Retrieval

**Milestone: Task Management Part 1**

- [x] Define task data structure
- [x] Define task API requirements
- [x] Design six task API test cases
- [x] Add in-memory task storage
- [x] Add automatic task ID generation
- [x] Implement `POST /tasks`
- [x] Implement `GET /tasks`
- [x] Support optional task descriptions
- [x] Reject empty and whitespace-only titles
- [x] Validate missing required fields
- [x] Add automated task tests
- [x] Validate returned task lists
- [x] Update project documentation
- [x] Review and merge changes

**Milestone Result:** 20 passing automated tests.

---

### Future Milestones

| Milestone | Planned Features | Status |
|---|---|---|
| Day 5 | Get single task, update task, delete task | Planned |
| Phase 3 | pytest fixtures and test isolation | Planned |
| Phase 4 | MySQL integration | Planned |
| Phase 5 | Database validation | Planned |
| Phase 6 | Parameterized and data-driven testing | Planned |
| Phase 7 | Logging and HTML test reports | Planned |
| Phase 8 | GitHub Actions continuous integration | Planned |
| Phase 9 | AI-assisted test case generation | Planned |
| Phase 10 | AI-assisted failure analysis | Planned |
| Phase 11 | Performance testing | Planned |
| Phase 12 | Final documentation and project review | Planned |

---

## 12. Known Limitations

The current version is an educational prototype.

1. User information is stored in a Python list and disappears when the application restarts.
2. Task information is stored in a Python list and disappears when the application restarts.
3. Passwords are temporarily stored in plaintext.
4. Real credentials must not be used.
5. Authentication tokens and sessions are not yet implemented.
6. Task ownership is not yet connected to authenticated users.
7. Tests currently use manually selected usernames and task names.
8. Comprehensive pytest fixture-based test isolation has not yet been implemented.
9. Persistent database state is not yet validated.
10. CI workflows have not yet been integrated.
11. Performance testing has not yet been implemented.
12. AI-assisted testing features have not yet been integrated.

These limitations will be addressed during later development milestones.

---

## 13. Planned Improvements

### Backend Improvements

- Complete Task CRUD APIs.
- Implement `GET /tasks/{id}`.
- Implement `PUT /tasks/{id}`.
- Implement `DELETE /tasks/{id}`.
- Introduce secure password hashing.
- Add token-based authentication.
- Replace in-memory storage with MySQL.
- Improve API error handling.
- Connect tasks with authenticated users.

### Testing Improvements

- Introduce pytest fixtures for setup and teardown.
- Implement parameterized testing.
- Add reusable API client helpers.
- Improve test-data isolation.
- Add database validation.
- Generate HTML test reports.
- Introduce structured logging.
- Expand boundary and negative test coverage.

### Automation Improvements

- Configure GitHub Actions.
- Automatically run regression tests on pull requests.
- Archive test results.
- Add performance testing with Locust.

### AI-Assisted Testing Improvements

- Generate candidate test scenarios from API specifications using an LLM.
- Validate generated test cases using rule-based checks.
- Require human review before generated cases enter the automated test suite.
- Collect failed test names, status codes, response bodies, exceptions, and logs.
- Use structured failure information for AI-assisted failure analysis.
- Generate possible root causes and investigation suggestions.
- Evaluate AI suggestions through human verification.

---

## 14. Learning Outcomes

Through this project, the team is developing practical understanding of:

- Python programming
- RESTful API design
- HTTP request and response handling
- FastAPI development
- Pydantic data validation
- CRUD concepts
- Functional testing
- Negative testing
- Boundary testing
- Automated API testing using pytest
- Test case design
- Test setup
- Test-data isolation concepts
- JSON object and list validation
- HTTP status codes
- Basic debugging and defect analysis
- Git version control
- GitHub collaboration
- Branch-based development
- Pull requests
- Peer code review
- Regression testing

Future stages will extend these learning outcomes into:

- SQL and MySQL
- Database validation
- pytest fixtures
- Parameterized testing
- Continuous integration
- Test reporting
- Performance testing
- AI-assisted software testing

---

## 15. Project Status

**Current Version:** Day 4 — Task Creation and Retrieval

**Implemented APIs:** 5

```text
GET  /health
POST /register
POST /login
POST /tasks
GET  /tasks
```

**Automated Test Cases:** 20

**Backend:** FastAPI with temporary in-memory user and task storage

**Testing:** pytest + FastAPI TestClient

**Current Completed Features:**

- Health check
- User registration
- User login
- Task creation
- Task retrieval
- Functional testing
- Negative testing
- Basic boundary testing
- Regression testing
- GitHub branch and pull request workflow

**Next Milestone:** Complete Task CRUD using:

```text
GET    /tasks/{id}
PUT    /tasks/{id}
DELETE /tasks/{id}
```

---

**AutoTest** is an educational and portfolio-oriented project focused on developing practical software testing, backend development, and test automation skills through collaborative engineering.
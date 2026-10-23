# AutoTest — RESTful API Automated Testing Project

A lightweight RESTful API service and automated testing project built with **Python, FastAPI, and pytest**.

## 1. Project Overview

AutoTest is a collaborative software development and quality assurance project designed to explore backend development, RESTful API testing, automated test execution, and software testing practices.

The project consists of two major components:

1. **Backend Service:** A lightweight task management service providing user registration, authentication, and task management APIs.
2. **Automated Testing:** A pytest-based testing suite that validates API functionality, response status codes, input validation, and error handling.

The long-term goal is to develop a maintainable automated API testing framework integrated with database validation, test reporting, and continuous integration.

### Project Objectives

- Develop RESTful APIs using FastAPI.
- Design functional, negative, and boundary test cases.
- Implement automated API tests using pytest.
- Validate HTTP status codes and JSON responses.
- Practice collaborative development using Git and GitHub.
- Improve test reliability, maintainability, and code quality.
- Integrate database verification, CI/CD, and performance testing in later stages.

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
              +--------+--------+
              |                 |
              v                 v
        Registration       Login Validation
              |                 |
              +--------+--------+
                       |
                       v
             In-Memory User Storage
                  (Temporary)


             Automated Test Suite
                       |
                       v
                  pytest Tests
                       |
            +----------+----------+
            |                     |
            v                     v
       HTTP Status           JSON Response
        Validation            Validation
            |                     |
            +----------+----------+
                       |
                       v
                   PASS / FAIL
```

**Current Implementation:** User registration and login functionality are implemented using in-memory user storage.

**Current Authentication:** Login verifies submitted credentials against registered users. Token-based authentication and session management have not yet been implemented.

**Future Implementation:** MySQL will replace in-memory storage and support database-level test validation. Password hashing and token-based authentication will also be introduced.

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
| `.gitignore` | Excludes virtual environments and temporary files |
| `requirements.txt` | Python package dependencies |
| `README.md` | Project documentation |

The project structure will be extended as additional APIs and automated testing features are implemented.

## 5. Installation and Setup

### Prerequisites

Ensure the following tools are installed:

- Python 3.11 or later (using a supported version)
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

The current project depends on FastAPI, pytest, and the dependencies required by FastAPI's TestClient.

### Step 4: Start the FastAPI Server

Run the following command from the project root:

```bash
fastapi dev app/main.py
```

The local development server should be accessible at:

```text
http://127.0.0.1:8000
```

### Step 5: Access the Interactive API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically generates interactive API documentation that can be used to inspect and manually test available endpoints.

## 6. Implemented RESTful APIs

The following endpoints are implemented in the Day 1–3 version.

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/health` | Check API service availability | 200 |
| POST | `/register` | Register a new user | 201 |
| POST | `/login` | Validate user credentials | 200 |

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

This endpoint is used to verify that the FastAPI application is running and responding to requests.

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

For example:

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

### 6.3 User Login API

**Endpoint:**

```http
POST /login
```

The login endpoint verifies the username and password of an existing registered user.

Unlike the registration endpoint, login does not create a new user. It validates the submitted credentials against the user information currently stored in memory.

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

A successful login requires:

- The username exists in the registered user list.
- The submitted password matches the stored password.
- Both input fields contain valid non-empty values.

The successful login response does not include the password.

**Incorrect Password:**

Status: `401 Unauthorized`

```json
{
  "detail": "Invalid username or password"
}
```

**Non-Existing Username:**

Status: `401 Unauthorized`

```json
{
  "detail": "Invalid username or password"
}
```

The same error message is used for incorrect passwords and unknown usernames to avoid revealing whether a particular username exists.

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

**Whitespace-Only Username:**

Status: `400 Bad Request`

```json
{
  "detail": "Username cannot be empty"
}
```

**Missing Required Field:**

Status: `422 Unprocessable Content`

For example:

```json
{
  "username": "alice"
}
```

Since `password` is a required field in the Pydantic request model, FastAPI automatically rejects the request.

### Current Login Rules

- Username is required.
- Password is required.
- Empty usernames are rejected.
- Empty passwords are rejected.
- Whitespace-only usernames are rejected.
- Leading and trailing whitespace is removed from usernames.
- The submitted username must exist in the registered user list.
- The submitted password must match the stored password.
- Incorrect usernames and passwords return `401 Unauthorized`.
- Successful login responses do not include passwords.
- Login currently performs credential validation only; authentication tokens are not issued.

### Login Workflow

```text
POST /login
     |
     v
Receive Username and Password
     |
     v
Pydantic Request Validation
     |
     +---- Missing Required Field ----> 422
     |
     v
Check Empty Input
     |
     +---- Empty Username/Password ---> 400
     |
     v
Search Registered Users
     |
     +---- Username Not Found --------> 401
     |
     v
Compare Password
     |
     +---- Incorrect Password --------> 401
     |
     v
Successful Login
     |
     v
200 OK
```

**Security Limitation:** The current educational prototype temporarily stores passwords in plaintext in memory and compares credentials directly. This implementation must not be used with real credentials or exposed as a production authentication service. Password hashing, persistent storage, and token-based authentication are planned improvements.

## 7. Automated API Testing

Automated tests are implemented using **pytest** and **FastAPI TestClient**.

The tests verify API behavior by comparing actual responses with predefined expected results.

### Testing Workflow

```text
Define Test Case
       |
       v
Prepare Test Data
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

### 7.1 Health Check Test

File: `tests/test_health.py`

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

This test validates:

- The health endpoint is accessible.
- HTTP status code is `200`.
- The response body contains the expected JSON data.

### 7.2 Registration API Tests

File: `tests/test_register.py`

The registration tests cover successful registration, invalid inputs, duplicate usernames, and missing required fields.

| Test ID | Test Scenario | Expected Status |
|---|---|---|
| TC001 | Register with valid username and password | 201 |
| TC002 | Register with an existing username | 400 |
| TC003 | Register with an empty username | 400 |
| TC004 | Register with an empty password | 400 |
| TC005 | Register with whitespace-only username | 400 |
| TC006 | Register without a password field | 422 |

The successful registration test also verifies that passwords are not included in API responses.

### 7.3 Login API Tests

File: `tests/test_login.py`

The login tests cover successful authentication, invalid credentials, empty inputs, and missing required fields.

| Test ID | Test Scenario | Expected Status |
|---|---|---|
| LOGIN001 | Login with valid username and password | 200 |
| LOGIN002 | Login with an incorrect password | 401 |
| LOGIN003 | Login with a non-existing username | 401 |
| LOGIN004 | Login with an empty username | 400 |
| LOGIN005 | Login with an empty password | 400 |
| LOGIN006 | Login with whitespace-only username | 400 |
| LOGIN007 | Login without a password field | 422 |

**Total Login Tests: 7**

### Login Test Setup

Unlike registration tests, successful login tests require a registered user to exist before the login request is executed.

A helper function is used to prepare the required test user.

```python
def register_test_user(username, password="123456"):
    response = client.post(
        "/register",
        json={
            "username": username,
            "password": password
        }
    )

    assert response.status_code == 201
```

This helper function creates a user before the login test.

For example:

```python
def test_login_success():
    register_test_user(
        "login_success_user",
        "123456"
    )

    response = client.post(
        "/login",
        json={
            "username": "login_success_user",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Login successful",
        "username": "login_success_user"
    }

    assert "password" not in response.json()
```

### Login Test Execution Flow

```text
Start Login Test
       |
       v
Register Test User
       |
       v
Verify Registration Success
       |
       v
Send Login Request
       |
       v
Receive Login Response
       |
       v
Verify Status Code
       |
       v
Verify JSON Response
       |
       v
    PASS / FAIL
```

This introduces the concept of **test setup**, where necessary data or conditions are prepared before testing a specific function.

### 7.4 Running Automated Tests

From the project root:

```bash
python -m pytest -q
```

Verified result for the completed Day 3 version:

```text
14 passed
```

The automated test suite currently contains:

- 1 health check test
- 6 user registration tests
- 7 user login tests

**Total: 14 automated tests**

All 14 tests have been successfully executed and passed during Day 3 verification.

### 7.5 Example Test Failure

Suppose a login test expects:

```text
Expected HTTP Status: 401
```

But the server returns:

```text
Actual HTTP Status: 200
```

pytest reports a failure.

This may indicate that invalid credentials were incorrectly accepted by the login endpoint.

Automated tests help identify behavior that is inconsistent with the API specification.

Test failures should be investigated against the agreed requirements instead of changing expected results merely to make tests pass.

## 8. Testing Strategy

The project follows a lightweight test-first development approach.

### Functional Testing

Verify that valid requests produce the expected results.

Examples:

- A new user can register successfully.
- An existing user can log in with valid credentials.
- Successful API responses contain the expected JSON data.

### Negative Testing

Verify that the API rejects invalid requests.

Examples:

- Duplicate username
- Empty password
- Missing required field
- Incorrect login password
- Non-existing login username

### Boundary Testing

Verify behavior around input limits and special values.

Current examples:

- Empty usernames
- Whitespace-only usernames
- Empty passwords

Future scenarios may include:

- Maximum username length
- Minimum password length
- Oversized request bodies
- Invalid data types

### Authentication Testing

Verify that login requests follow the expected credential validation rules.

Current scenarios include:

- Valid username and password
- Incorrect password
- Unknown username
- Missing login fields
- Invalid empty input

Token validation, expiration, and authorization testing will be introduced in later development stages.

### Test Setup

Some tests require existing application data.

For example, a successful login test requires a registered user.

A reusable registration helper is used to create the necessary test user before login validation.

In later stages, pytest fixtures will be introduced to manage test setup and teardown more systematically.

### Regression Testing

Previously implemented tests are executed again after changes to ensure existing functionality still works.

For example:

- Day 1 health tests continue running after registration and login are added.
- Day 2 registration tests continue running after the login API is implemented.
- Day 3 login tests are added to the existing regression test suite.

The complete suite currently contains 14 tests.

## 9. Development Workflow

The project uses Git and GitHub for collaborative development.

```text
Requirements
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
Execute Tests
     |
     +---- FAIL (Expected Before Implementation)
     |
     v
Implement API
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

### Git Commands

Create a feature branch:

```bash
git checkout -b feature/login
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
git commit -m "implement login API and tests"
```

Push the branch:

```bash
git push -u origin feature/login
```

After a pull request is reviewed and merged:

```bash
git checkout main

git pull origin main
```

Run regression tests again:

```bash
python -m pytest -q
```

The `main` branch should remain in a working, tested state.

## 10. Team Collaboration

This project is developed by a two-person team.

Both members contribute to backend development, automated testing, debugging, and code reviews.

### Primary Responsibilities

| Role | Primary Focus | Secondary Focus |
|---|---|---|
| Member A | Automated testing and test design | Backend development |
| Member B | Backend and API implementation | Automated testing |

Responsibilities are rotated across features so that both members gain practical experience with the complete development and testing workflow.

### Day 1 Responsibilities

| Member A | Member B |
|---|---|
| Project initialization | pytest setup |
| FastAPI health endpoint | Health endpoint test |
| Branch and PR workflow | Test execution and review |

### Day 2 Responsibilities

| Member A | Member B |
|---|---|
| Registration API test design | Registration API implementation |
| Registration automated tests | Request validation and error handling |
| Test execution and verification | Backend debugging |
| Backend code review | Test code review |

### Day 3 Responsibilities

| Member A | Member B |
|---|---|
| Login API implementation | Login API test design |
| Credential validation logic | Login automated tests |
| HTTP status and error handling | Test setup helper implementation |
| Backend debugging | Test execution and verification |
| Test code review | Backend code review |

During Day 3, the primary development and testing roles were exchanged.

This allows both team members to gain experience implementing backend functionality and designing automated tests.

### Collaboration Principles

- Use a shared GitHub repository.
- Create branches for new features.
- Define API requirements before implementation.
- Write automated tests for implemented functionality.
- Review code before merging into `main`.
- Keep the main branch functional.
- Ensure both members understand major technical decisions.
- Rotate development and testing responsibilities across project milestones.

## 11. Development Progress

### Day 1 — Project Initialization

**Milestone: Project Bootstrap**

- [x] Create GitHub repository
- [x] Configure local development environments
- [x] Create Python virtual environments
- [x] Install FastAPI and pytest
- [x] Establish the project directory structure
- [x] Implement `GET /health`
- [x] Create the first automated test
- [x] Verify successful test execution
- [x] Practice Git branching and commits
- [x] Create and review a pull request
- [x] Merge changes into `main`

**Milestone Result:** 1 passing automated test.

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

### Day 3 — User Login

**Milestone: Login API and Automated Tests**

- [x] Define login API requirements
- [x] Design seven login test cases
- [x] Implement `POST /login`
- [x] Add Pydantic login request validation
- [x] Implement username lookup
- [x] Implement password comparison
- [x] Handle incorrect passwords with HTTP 401
- [x] Handle non-existing users with HTTP 401
- [x] Reject empty username and password inputs
- [x] Validate missing required fields
- [x] Create login test setup helper
- [x] Add automated login tests
- [x] Verify successful and failed login responses
- [x] Run complete regression test suite
- [x] Verify all 14 automated tests pass

**Milestone Result:** 14 passing automated tests.

### Future Milestones

| Milestone | Planned Features | Status |
|---|---|---|
| Day 4 | Task creation and retrieval APIs | Planned |
| Phase 2 | Complete Task CRUD API and tests | Planned |
| Phase 3 | MySQL integration | Planned |
| Phase 4 | Database validation | Planned |
| Phase 5 | pytest fixtures and parameterization | Planned |
| Phase 6 | Logging and HTML test reports | Planned |
| Phase 7 | GitHub Actions continuous integration | Planned |
| Phase 8 | Performance testing | Planned |
| Phase 9 | Final documentation and project review | Planned |

## 12. Known Limitations

The current version is an early educational prototype.

1. User information is stored in a Python list and disappears after the application restarts.
2. Passwords are temporarily stored in plaintext. Real credentials must not be used.
3. Login performs credential validation only. Authentication tokens and session management are not implemented.
4. Tests currently use manually selected usernames and do not yet implement comprehensive test-data isolation.
5. Login tests require registered users to be prepared before execution.
6. Tests do not yet validate persistent database state.
7. Automated CI workflows have not yet been integrated.
8. Performance testing has not yet been implemented.
9. Task management APIs have not yet been implemented.
10. The current authentication implementation is for local educational testing only and is not suitable for production deployment.

These limitations will be addressed during later development milestones.

## 13. Planned Improvements

### Backend Improvements

- Introduce secure password hashing.
- Add token-based authentication.
- Develop task CRUD endpoints.
- Replace in-memory storage with MySQL.
- Improve API error handling.
- Separate API routes and business logic into maintainable modules.

### Testing Improvements

- Introduce pytest fixtures for setup and teardown.
- Implement parameterized testing.
- Add reusable API client helpers.
- Improve test-data isolation.
- Add database validation.
- Generate HTML test reports.
- Introduce structured logging.
- Expand negative and boundary test coverage.

### Automation Improvements

- Configure GitHub Actions.
- Automatically run regression tests on pull requests.
- Archive test results.
- Add performance testing with Locust.

## 14. Learning Outcomes

Through this project, the team aims to develop practical understanding of:

- Python programming
- RESTful API design
- HTTP request and response handling
- FastAPI development
- Pydantic data validation
- Functional and negative testing
- Automated API testing using pytest
- Test case design
- Basic debugging and defect analysis
- Git version control
- GitHub collaboration
- Code review workflows
- Regression testing
- User registration and login workflows
- Basic authentication logic
- HTTP 401 error handling
- Test setup and reusable helper functions
- Multi-endpoint integration testing

## 15. Project Status

**Current Version:** Day 3 — User Login

**Implemented APIs:** 3

**Automated Test Cases:** 14

**Test Execution Result:** 14 passed

**Backend:** FastAPI with in-memory user storage

**Authentication:** Basic username and password validation (no token/session management)

**Testing:** pytest + FastAPI TestClient

**Completed Milestones:**

- Day 1 — Project Initialization
- Day 2 — User Registration
- Day 3 — User Login

**Next Milestone:** Task Creation and Retrieval APIs (`POST /tasks` and `GET /tasks`)

---

**AutoTest** is an educational and portfolio-oriented project focused on developing practical software testing and test automation skills through collaborative engineering.

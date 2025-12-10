## **Assignment 12 – User & Calculation Routes + Integration Testing**

**Author:** Nandan Kumar
---

## **Introduction**

In this assignment, I extended my FastAPI application by implementing fully operational **User Authentication (Register/Login)** and complete **Calculation CRUD (Browse, Read, Edit, Add, Delete)** routes. These routes are validated using strict Pydantic schemas, backed by SQLAlchemy models, protected using secure JWT authentication, and tested with full integration coverage using pytest.

I also expanded my CI/CD pipeline so that every commit automatically runs database-backed integration tests in GitHub Actions, builds & scans the Docker image using Trivy, and finally deploys a production-ready container to Docker Hub.
This assignment completes the back-end portion of the modular calculator application and prepares the foundation for UI integration in the next module.

---

## **Project Structure and Tools**

The project includes five core components:

| Component       | Purpose                                   |
| --------------- | ----------------------------------------- |
| **app/auth**    | JWT authentication, hashing, dependencies |
| **app/routers** | User & Calculation API route handlers     |
| **app/models**  | SQLAlchemy User & Calculation models      |
| **app/schemas** | Pydantic v2 schemas for validation        |
| **tests/**      | Unit + integration + e2e tests            |

### **Main Technologies Used**

* **FastAPI** – REST API backend
* **SQLAlchemy ORM** – Database modeling
* **Pydantic v2** – Validation & serialization
* **JWT Authentication** – Secure login system
* **Docker + Docker Compose** – Fully containerized environment
* **PostgreSQL + pgAdmin** – Database services
* **pytest + pytest-cov** – Integration/coverage testing
* **GitHub Actions** – CI/CD automation
* **Trivy** – Container vulnerability scanning

---

## **Running the Project with Docker**

Start all services:

```bash
docker compose up --build
```

Access:

* FastAPI UI → [http://localhost:8000](http://localhost:8000)
* Swagger Docs → [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc Docs → [http://localhost:8000/redoc](http://localhost:8000/redoc)
* pgAdmin → [http://localhost:5050](http://localhost:5050)

Stop everything:

```bash
docker compose down
```

---

## **Key Features Implemented**

###  **User Authentication**

* **POST /auth/register** — Create a user using `UserCreate`
* **POST /auth/login** — Validate password, return JWT token
* **GET /auth/me** — Retrieve current user via token

###  **Calculation CRUD (BREAD Operations)**

| Action | Method & Route         | Description                      |
| ------ | ---------------------- | -------------------------------- |
| Browse | **GET /calc/all**      | List all calculations for a user |
| Read   | **GET /calc/{id}**     | Retrieve a single calculation    |
| Edit   | **PUT /calc/{id}**     | Update existing calculation      |
| Add    | **POST /calc/compute** | Perform + store a calculation    |
| Delete | **DELETE /calc/{id}**  | Remove an entry                  |

All endpoints enforce:

* JWT authentication
* Pydantic validation
* Division-by-zero protection
* Clean, consistent response schemas

---

## **Pydantic Schema Highlights**

### **UserCreate**

* Validates username, password strength, email format
* Prevents weak/invalid credentials

### **CalculationCreate**

* Accepts `type`, `a`, `b`
* Auto-computes `result`
* Rejects unsupported types
* Division-by-zero error → `"Division by zero"`

---

## **Testing (Pytest + Coverage)**

###  Integration tests cover:

* User registration & login
* JWT token decoding
* Authentication dependency behavior
* Calculation CRUD workflow
* Invalid inputs & negative test cases
* Schema behaviors (auto-result, validators, etc.)

###  Local test command:

```bash
pytest --cov=app -v
```

###  Coverage Requirement

CI/CD enforces:

```
--cov-fail-under=90
```

Local result: **96% total coverage**

---

## **CI/CD Pipeline (GitHub Actions)**

The workflow includes three automated stages:

---

### **1. Test Stage — PostgreSQL + Integration Tests**

* Spins up PostgreSQL service in GitHub Actions
* Installs project dependencies
* Runs all integration tests (except e2e)
* Enforces ≥90% coverage

### **2. Security Stage — Trivy Scan**

* Builds Docker image
* Scans for HIGH + CRITICAL vulnerabilities
* Pipeline fails if unsafe

### **3. Deployment Stage — Docker Hub Push**

* Builds final production image
* Pushes to Docker Hub:

```
nandanksingh/module12_user_calculation_routes_integration_testing:img_m12
```

---

## **Docker Hub Deployment**

Repository:
[https://hub.docker.com/r/nandanksingh/module12_user_calculation_routes_integration_testing](https://hub.docker.com/r/nandanksingh/module12_user_calculation_routes_integration_testing)

Pull image:

```bash
docker pull nandanksingh/module12_user_calculation_routes_integration_testing:img_m12
```

Run:

```bash
docker run -d -p 8000:8000 nandanksingh/module12_user_calculation_routes_integration_testing:img_m12
```

---

## **Local Development Setup (Without Docker)**

```bash
git clone https://github.com/nandanksingh/IS601_Assignment12.git
cd IS601_Assignment12
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Access Swagger Docs:

```
http://localhost:8000/docs
```

---

## **Manual Testing Using Swagger / ReDoc**

### Test User Endpoints

1. Register a new user
2. Log in → receive JWT
3. Use JWT in **Authorize → Bearer token**

### Test Calculation Endpoints

* Add → Subtract → Multiply → Divide
* Check returned `result`
* Try division by zero error
* Edit an existing calculation
* Delete a calculation

---

## **Common Problems and Fixes**

| Problem                                 | Reason                      | Fix                                                                        |
| --------------------------------------- | --------------------------- | -------------------------------------------------------------------------- |
| Missing JWT token                       | Dependency mismatch         | Rewrote `get_current_user` to accept `token: str = Depends(oauth2_scheme)` |
| Swagger Docs not loading inside Docker  | Wrong template path         | Moved templates to `/templates` root                                       |
| “Internal Server Error” on root route   | Wrong Jinja path            | Updated to `Jinja2Templates(directory="templates")`                        |
| Docker image failed to push             | Incorrect naming convention | Standardized tag: `img_m12`                                                |
| GitHub Actions failing to connect to DB | DB not ready                | Added 30-second retry loop + health checks                                 |

---

## **Reflection**

Completing this module gave me hands-on experience building a real authentication system and connecting it to fully functional API routes. Implementing user registration and secure password handling made me appreciate the importance of validation, hashing, and predictable error responses. Working with JWT tokens taught me how modern APIs manage identity without storing session state.

The biggest challenge was getting all integration tests to pass with high coverage. Several failures came from tiny issues—like incorrect token dependency signatures, missing validators, or mismatched field names. Fixing these required careful reading of test expectations and refining the logic until every edge case was handled consistently.

Docker integration also created some problems, especially around template paths and container health checks. I learned how sensitive containerized applications are to directory structure and environment variables. Updating my CI/CD pipeline to build, test, scan, and deploy the project gave me a much clearer understanding of DevOps workflows and how automated testing ensures software reliability.

Overall, this module strengthened my skills in backend API design, authentication, testing, database integration, and cloud-ready deployment. It sets up everything needed for the front-end integration that comes next.

---

## **Final Summary**

This module delivered:

* Full **User Authentication** with secure JWT
* Complete **Calculation CRUD** routes
* Strict **Pydantic validation**
* Strong **integration testing** with 96% coverage
* Reliable **PostgreSQL-backed CI pipeline**
* Automated **Docker build + push** to Docker Hub
* Fully functional web UI inside Docker

This project delivers a complete backend service with **secure authentication**, **full calculation CRUD**, **comprehensive integration tests**, **CI/CD automation**, and **Dockerized deployment**. It represents a major milestone in building reliable, production-ready Python APIs, and prepares the foundation for future front-end integration.


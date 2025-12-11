# **Assignment 13 – JWT Authentication, Front-End Integration & Playwright E2E Testing**
**Author:** Nandan Kumar
---

## ** Introduction**
---
In Assignment 13, I developed a fully functional JWT-based authentication system that integrates backend APIs, frontend pages, and automated end-to-end testing into a single cohesive workflow. The backend now supports secure registration and login with password hashing, duplicate-user checks, and JWT token generation. On the frontend, I implemented complete login and registration pages using HTML/CSS/JS, including client-side checks for required fields, email formatting, and password strength.

Playwright E2E tests validate real user behavior—covering both successful flows and error scenarios—ensuring the UI and backend communicate correctly. All tests (unit, integration, and E2E) run automatically inside GitHub Actions. Once tests pass, a production Docker image is built and pushed to Docker Hub, creating a fully automated CI/CD pipeline.

This assignment establishes the authentication foundation for the project. In Module 14, I will extend this by adding full BREAD calculation functionality to the frontend using the JWT-secured routes implemented here.

---

# ** Project Structure Overview**

| Component          | Purpose                                          |
| ------------------ | ------------------------------------------------ |
| **app/auth**       | Password hashing, JWT creation, token validation |
| **app/routers**    | Routes for `/auth` and UI pages                  |
| **app/models**     | SQLAlchemy user model & DB mapping               |
| **app/schemas**    | Pydantic v2 schemas for registration/login       |
| **templates/**     | All HTML pages used by the front-end             |
| **static/**        | CSS + JavaScript for UI behavior                 |
| **tests/**         | Unit, integration, and Playwright E2E tests      |
| **Docker + CI/CD** | Automated test + build + deploy pipeline         |

### **HTML Templates Included**

```
templates/
├── base.html
├── layout.html
├── index.html
├── login.html
├── register.html
└── dashboard.html
```

### **Static Files**

```
static/css/style.css
static/js/script.js
```

---

# ** Running the Project With Docker (Recommended)**

### **Start all services**

```bash
docker compose up --build
```

### **Access the app**

* App Homepage → [http://localhost:8000](http://localhost:8000)
* Login Page → [http://localhost:8000/login](http://localhost:8000/login)
* Register Page → [http://localhost:8000/register](http://localhost:8000/register)
* Dashboard (requires JWT) → [http://localhost:8000/dashboard](http://localhost:8000/dashboard)
* Swagger Docs → [http://localhost:8000/docs](http://localhost:8000/docs)

### **Stop**

```bash
docker compose down
```

---

# ** Local Development Without Docker**

You can run the backend locally using:

```bash
git clone https://github.com/nandanksingh/IS601_Assignment13
cd IS601_Assignment13
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
uvicorn main:app --reload
```

### **Common Local Run Problems & Fixes**

| Problem                 | Reason                                               | Fix                                                            |
| ----------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| Templates not rendering | Wrong path                                           | Ensure: `Jinja2Templates(directory="templates")`               |
| CSS/JS 404 errors       | Incorrect static mount                               | Verify: `app.mount("/static", StaticFiles(directory="static")` |
| JWT not stored          | JS errors                                            | Check console → script.js load path                            |
| Login page reload loop  | Missing `localStorage.getItem("access_token")` check | Re-add redirect logic                                          |
| Uvicorn runs twice      | VSCode auto-reload conflict                          | Add: `"reload": true` in launch config                         |
| DB errors               | Old SQLite file                                      | Delete `test.db` and restart                                   |

---

# ** JWT Authentication Features Implemented**

### **Registration — `/auth/register`**

* Accepts user info: username, email, mobile, password, confirm password
* Validates with Pydantic (strong password, valid email, 10-digit mobile)
* Hashes password securely using bcrypt
* Stores user in database
* Returns a success message

### **Login — `/auth/login`**

* Accepts identifier (email OR mobile) + password
* Validates user & password
* Returns a **JWT access token**
* Token stored in **localStorage** on the front-end

### **Current User — `/auth/me`**

* Uses token from `Authorization: Bearer <token>`
* Returns the authenticated user profile

---

# ** Front-End Pages Implemented**

### **`index.html` – Home Page**

* Public landing page
* Redirects authenticated users to dashboard

### **`register.html`**

* Client-side validations:

  * Valid email
  * Minimum 6-character password
  * Password confirmation
* On success → registration success message

### **`login.html`**

* Checks required fields
* Fetch API sends credentials
* On success → JWT stored in `localStorage` → redirect to dashboard

### **`dashboard.html`**

* Accessible only when JWT is present
* Includes logout logic

### **Shared Layout**

* `base.html` + `layout.html` manage styling & JS/CSS imports

---

# ** Testing**

## ** Unit + Integration Tests**

Covered:

* User creation & schema validation
* Password hashing + verification
* JWT creation + decoding
* Login/registration logic
* Database operations (SQLite/Postgres)

Run:

```bash
pytest --cov=app -v
```

Coverage enforced:

```
--cov-fail-under=90
```

## ** Playwright End-to-End Tests**

E2E tests verify:

* Successful registration
* Failed registration (short password, invalid email)
* Login success
* Login failure (wrong password / unknown user)
* UI error messages
* Token saved to browser storage

Run locally:

```bash
pytest -m e2e
```

---

# ** CI/CD Pipeline (GitHub Actions)**

On every commit:

### **1. Install & Test**

* Installs dependencies
* Spins up database
* Runs unit + integration + e2e tests
* Enforces ≥90% coverage

### **2. Build & Scan Image**

* Docker build
* Trivy vulnerability scan
* Pipeline fails on HIGH or CRITICAL issues

### **3. Push to Docker Hub**

Image:

```
nandanksingh/module13_fastapi_jwt_auth:img_m13
```

Docker Hub:
[https://hub.docker.com/r/nandanksingh/module13_fastapi_jwt_auth](https://hub.docker.com/r/nandanksingh/module13_fastapi_jwt_auth)

---

# ** Reflection**

Working on Assignment 13 helped me understand how backend authentication, frontend validation, and full-stack testing come together to form a secure and user-friendly login system. Implementing JWT-based login and registration gave me a deeper appreciation for stateless authentication and how tokens enable secure access without storing sessions on the server. Building the front-end pages made me think more carefully about user experience—especially how helpful client-side checks can be in reducing errors before data even reaches the server.

Playwright E2E testing was one of the most valuable parts of this module. It allowed me to validate the entire user journey, from typing into form fields to receiving meaningful error messages. Testing both valid and invalid scenarios clarified how important consistent server responses are when building real-world applications.

I faced a few challenges with JWT verification, token storage, and ensuring Docker had the correct paths for templates and static files. Playwright also required precise selectors to target input fields and buttons. Step by step, I resolved these issues by reviewing logs, adding clear client-side validation, and refining my routes to match expected behaviors. Overall, this module strengthened my full-stack confidence.

---

# ** Conclusion **

Assignment 13 brought together many skills from previous modules and turned them into a fully functional authentication system. By building registration and login pages, validating user input, generating JWTs, and protecting routes, I learned how real applications manage secure access. Adding Playwright E2E tests ensured the system works exactly as intended, both visually and functionally, from the user’s point of view. Integrating everything into a Docker and CI/CD setup showed me how professional workflows automate testing and deployment. This module not only improved my technical skills but also gave me a strong understanding of how backend systems, front-end interfaces, automated testing, and DevOps pipelines all work together in modern software development.

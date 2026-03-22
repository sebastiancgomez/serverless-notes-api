# 📝 Serverless Notes API

A **serverless REST API** for managing notes, built with **AWS Lambda**, **Python**, and **SQLAlchemy**, featuring **JWT authentication**, role-based access control, and full **CRUD operations**.

This project was built as a hands-on exercise to demonstrate practical knowledge of serverless architecture, Python backend development, and AWS Lambda patterns applicable to high-volume transactional systems.

---

## 🚀 Live API

The API is publicly available at:

```
https://zeoi4yrka3.execute-api.us-east-2.amazonaws.com/default/notes/
```

> ⚠️ Authentication required — use the login endpoint to obtain a JWT token before calling other endpoints.

---

## ✨ Features

- 🔐 JWT Authentication (login endpoint)
- 📄 Full CRUD — Create, Read, and Delete notes
- 👤 User-based access control
- 🛡️ Role-based authorization:
  - Users can only access their own notes
  - Admins can access all notes
- 🧪 Unit tests with `pytest`
- 📊 Code coverage support

---

## 🏗️ Architecture

The service follows a clean layered architecture:

```
API Gateway Event
       ↓
lambda_handler.py       ← AWS Lambda entrypoint
       ↓
service/app/
 ├── router.py          ← Request routing (API Gateway style)
 ├── service.py         ← Business logic
 ├── repository.py      ← Data access layer (SQLAlchemy)
 ├── auth.py            ← JWT & authentication logic
 ├── db_models.py       ← SQLAlchemy models
 ├── database.py        ← Engine & session management
 └── exceptions.py      ← Custom exceptions
```

**Design principles applied:**
- Stateless design — each Lambda invocation is independent
- Separation of concerns — routing, business logic, and data access are fully decoupled
- Secure by default — all endpoints except login require a valid JWT token

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.12+ |
| Compute | AWS Lambda |
| API Layer | AWS API Gateway |
| ORM | SQLAlchemy |
| Auth | JWT (PyJWT) |
| Database (local/test) | SQLite |
| Testing | Pytest + Coverage |

> **Note on database:** SQLite is used for simplicity and local testing. A production deployment would use **Amazon DynamoDB** or **Amazon RDS (PostgreSQL)** depending on the access patterns — DynamoDB for high-throughput key-value operations, RDS for relational queries.

---

## 🔑 Authentication

### Login

```
POST /default/auth/login
```

```json
{
  "username": "sebastian",
  "password": "123456"
}
```

Response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

Include the token in subsequent requests:

```
Authorization: Bearer <JWT_TOKEN>
```

---

## 📄 API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/default/auth/login` | Obtain JWT token | ❌ |
| GET | `/default/notes` | List notes | ✅ |
| GET | `/default/notes/{id}` | Get note by ID | ✅ |
| POST | `/default/notes` | Create note | ✅ |
| DELETE | `/default/notes/{id}` | Delete note | ✅ |

---

## 🧪 Testing with Postman

A ready-to-use Postman collection is available in the `/postman` folder.

Import it into Postman and run the requests in this order:
1. **Auth** — obtains a JWT token automatically saved as `{{token}}`
2. **Create** — creates a new note
3. **Notes** — lists your notes
4. **GET by ID** — retrieves a specific note
5. **Delete** — deletes a note

No manual token configuration needed — authentication is handled automatically.

---

## 🛡️ Authorization Rules

| Action | User | Admin |
|---|---|---|
| View own notes | ✅ | ✅ |
| View all notes | ❌ | ✅ |
| Delete own note | ✅ | ✅ |
| Delete any note | ❌ | ✅ |

---

## 🧪 Running Tests

```bash
pytest -v
```

### Coverage report

```bash
pytest --cov=service --cov-report=term-missing
pytest --cov=service --cov-report=html
```

---

## ⚙️ Environment Configuration

```bash
# Local development
export DATABASE_URL=sqlite:///./test.db

# AWS Lambda — must use /tmp (only writable directory)
DATABASE_URL=sqlite:////tmp/test.db
```

---

## ☁️ Deployment

This project runs on AWS Lambda using API Gateway events.

- **Entry point:** `lambda_handler.lambda_handler`
- **Stateless design** — no shared state between invocations
- **SQLite stored in `/tmp`** — Lambda's only writable directory

---

## 🧠 Design Decisions

- **Layered architecture** — Router → Service → Repository mirrors enterprise patterns applicable to production microservices
- **Manual routing** — simulates API Gateway behavior without a framework dependency
- **Stateless JWT auth** — no server-side session storage, scales naturally with Lambda's concurrency model
- **SQLite for portability** — allows full local development and testing without external dependencies; swap to DynamoDB or RDS for production
- **Test isolation** — in-memory database ensures tests are reproducible and independent

---

## 🔭 Future Improvements

- [ ] Migrate persistence to **DynamoDB** for production-grade scalability
- [ ] Add **PUT/PATCH** endpoint for note updates
- [ ] Implement **pagination** for notes listing
- [ ] Add **middleware** for centralized authentication
- [ ] **Docker** support for local development
- [ ] **GitHub Actions CI/CD** pipeline for automated deployment

---

## 👨‍💻 About the Author

**Juan Sebastián Cárdenas Gómez**
Senior Backend Engineer | Java | .NET | Python | Serverless | AWS | Cloud-native

15+ years building mission-critical backend systems in finance, insurance, and fintech.

- 🔗 GitHub: [github.com/sebastiancgomez](https://github.com/sebastiancgomez)
- 🔗 LinkedIn: [linkedin.com/in/sebastiancgomez](https://linkedin.com/in/sebastiancgomez)

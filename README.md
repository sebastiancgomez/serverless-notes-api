# 📝 Serverless Notes API

A **serverless REST API** for managing notes, built with **AWS Lambda**, **Python**, and **SQLAlchemy**, featuring **JWT authentication** and full **CRUD operations**.

---

## 🚀 Features

- 🔐 JWT Authentication (login endpoint)
- 📄 Create, Read, and Delete notes
- 👤 User-based access control
- 🛡️ Authorization rules:
  - Users can only access their own notes
  - Admins can access all notes
- 🧪 Unit tests with `pytest`
- 📊 Code coverage support

---

## 🏗️ Architecture

service/
│
├── app/
│   ├── router.py        # Request handling (API Gateway style)
│   ├── service.py       # Business logic
│   ├── repository.py    # Data access layer (SQLAlchemy)
│   ├── auth.py          # JWT & authentication logic
│   ├── db_models.py     # SQLAlchemy models
│   ├── database.py      # Engine & session management
│   └── exceptions.py    # Custom exceptions
│
├── lambda_handler.py    # AWS Lambda entrypoint

---

## ⚙️ Tech Stack

- Python 3.12+
- AWS Lambda
- API Gateway (event-based routing)
- SQLAlchemy
- SQLite (for local/testing)
- Pytest

---

## 🔑 Authentication

### Login

POST /default/auth/login

{
  "username": "sebastian",
  "password": "123456"
}

Response:

{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}

---

## 📄 Endpoints

GET /default/notes

GET /default/notes/{id}

POST /default/notes

{
  "title": "My note"
}

DELETE /default/notes/{id}

---

## 🛡️ Authorization Rules

| Action            | User | Admin |
|------------------|------|-------|
| View own notes   | ✅   | ✅    |
| View all notes   | ❌   | ✅    |
| Delete own note  | ✅   | ✅    |
| Delete any note  | ❌   | ✅    |

---

## 🧪 Running Tests

pytest -v

---

## 📊 Coverage

pytest --cov=service --cov-report=term-missing

pytest --cov=service --cov-report=html

---

## ⚙️ Environment Configuration

export DATABASE_URL=sqlite:///./test.db

For AWS Lambda:

DATABASE_URL=sqlite:////tmp/test.db

---

## ☁️ Deployment

This project is designed to run on AWS Lambda using API Gateway events.

- Entry point: lambda_handler.lambda_handler
- Stateless design
- SQLite stored in /tmp (Lambda constraint)

---

## 🧠 Design Decisions

- Layered architecture: Router → Service → Repository
- Manual routing to simulate API Gateway behavior
- Stateless authentication using JWT
- SQLite for simplicity and portability
- Test isolation using in-memory database

---

## 📌 Future Improvements

- ✏️ Update notes (PUT/PATCH)
- 📦 Pagination for notes
- 🧩 Middleware for authentication
- 🐳 Docker support
- ☁️ Integration with RDS or DynamoDB

---

## 👨‍💻 About the Author

**Juan Sebastián Cárdenas Gómez**
Senior Backend Engineer | Cloud (Azure) | Python | Serverless architecture | Cloud-native applications

15+ years building mission-critical backend systems in finance, insurance, and fintech.

- 🔗 GitHub: [github.com/sebastiancgomez](https://github.com/sebastiancgomez)
- 🔗 LinkedIn: [linkedin.com/in/sebastiancgomez](https://linkedin.com/in/sebastiancgomez)

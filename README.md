# 🚀 FastAPI Starter Kit

A modern, batteries-included FastAPI template designed for rapid development of scalable and maintainable APIs.

This template integrates the core tools and patterns needed for a production-ready backend — so you can skip the boilerplate and focus on building your app.

---

## ✨ Features

- **FastAPI** — High-performance web framework for building APIs with Python 3.11+
- **SQLAlchemy 2.0 (async)** — Fully asynchronous ORM using the new 2.0-style engine and session APIs
- **Pydantic v2** — Type-safe models for request validation and response serialization
- **JWT Authentication** — Secure, stateless access token flows
- **Alembic** — Database migrations with version control and auto-generation support
- **Async-first Design** — Built from the ground up for async I/O, database queries, and endpoints
- **Clean, Modular Codebase** — Scalable architecture ready for real-world applications

---

## 🛠️ Database Layer

Built with the latest SQLAlchemy 2.0 patterns, including:

- `async_engine` and `async_sessionmaker`
- Declarative model definitions
- Dependency-injected sessions using FastAPI's `Depends`
- Easy integration with Alembic for schema migrations

---

## 🧩 Extensibility

This template is designed to grow with your project. Add new controllers, services, models, and background tasks easily without reworking the foundation.

---

## 📦 Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2.0+
- Pydantic v2
- Alembic
- PostgreSQL (recommended, but not enforced)
- JWT Auth Flow

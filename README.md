# MOBREP – Mobile Banking Records

**MOBREP** is an asynchronous, audit-ready backend system for mobile banking operations, designed to log and manage teller transactions including overages and shortages. Built with **FastAPI**, **SQLModel**, and **SQLite** (with easy PostgreSQL migration).

---

---

## ⚡ Tech Stack

- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) (built on SQLAlchemy)
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Async**: Fully asynchronous with `async` / `await`
- **UUID**: All primary keys are UUIDs for audit-safe operations

---

## 🔧 Features

- **Tellers**: Full CRUD for managing teller accounts.
- **Users**: Admins, Managers, and Coordinators – full CRUD.
- **Transactions**: Append-only ledger of overages/shortages.
- **UUID-based IDs**: Secure and mobile-friendly.
- **Timezone-aware timestamps**: All dates stored in UTC.
- **Modular structure**: Clean separation of routers and DB logic.
- **OpenAPI docs**: Auto-generated Swagger UI at `/docs` and ReDoc at `/redoc`.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mobrep.git
cd mobrep

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\Activate.ps1 # Windows PowerShell

uvicorn app.main:app --reload
```

Swagger UI will be available at: http://127.0.0.1:8000/docs

ReDoc docs at: http://127.0.0.1:8000/redoc

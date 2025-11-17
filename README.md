# Library Management System - FastAPI Backend

Professional FastAPI backend for a library management system using MongoDB (Motor).

Overview
- Async FastAPI application with modular routers for `books`, `users`, and `loans`.
- Uses `motor` (async MongoDB driver) for non-blocking database access.
- Includes Docker and docker-compose to run the app alongside MongoDB.

Prerequisites
- Python 3.10+ or Docker & Docker Compose
- MongoDB (local or remote).

Quick start (local Python)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set MONGO_URI and MONGO_DB if needed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run with Docker Compose
```bash
docker compose up --build
```

Testing
- Unit tests are written with `pytest` and `pytest-asyncio` and mock database behaviors.
```bash
pip install -r requirements.txt
pytest -q
```

API Endpoints
- `POST /books` - Create a book (body: JSON with `title`, `author`, optional `isbn`, `copies`, `description`)
- `GET /books` - List books
- `GET /books/{id}` - Retrieve a book
- `PUT /books/{id}` - Update a book
- `DELETE /books/{id}` - Delete a book
- `POST /users` - Create a user
- `GET /users` - List users
- `POST /loans/borrow?user_id=<>&book_id=<>` - Borrow a book
- `POST /loans/return?loan_id=<>` - Return a book

Configuration
- Copy `.env.example` to `.env` and set `MONGO_URI` (e.g. `mongodb://mongo:27017` when using docker-compose) and `MONGO_DB` (database name).

Notes & Next Steps
- This repo includes a minimal authentication-free example. For production, add authentication, input validation hardening, logging, and more robust error handling.
- Optional: add CI for tests and a Docker image publish pipeline.

License
- MIT (or choose your preferred license)
# Library Management System - FastAPI Backend

Quick backend using FastAPI and MongoDB (Motor).

Requirements
- Python 3.10+
- MongoDB (or Mongo-compatible URI)

Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env to point to your MongoDB instance
```

Run
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API endpoints (examples)
- `POST /books` - add a book
- `GET /books` - list books
- `GET /books/{id}` - get book
- `PUT /books/{id}` - update book
- `DELETE /books/{id}` - delete book

Notes
- Uses `motor` (async MongoDB driver) and environment variables from `.env`.# library-management-system-backend
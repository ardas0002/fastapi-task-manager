# FastAPI Task Manager

A simple task management REST API built with FastAPI and SQLModel.

## Tech Stack

- **FastAPI** - web framework
- **SQLModel** - ORM (SQLAlchemy + Pydantic)
- **SQLite** - database
- **Uvicorn** - ASGI server

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -e .
```

## Run

```bash
python -m app.main
```

API will be available at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/tasks` | Create a new task |
| GET | `/tasks` | List tasks (with filtering & pagination) |
| GET | `/tasks/{id}` | Get task by ID |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

### Query Parameters for `GET /tasks`

| Parameter | Type | Description |
|-----------|------|-------------|
| `completed` | bool | Filter by completion status |
| `search` | string | Search by title |
| `skip` | int | Offset for pagination (default: 0) |
| `limit` | int | Items per page (default: 10, max: 100) |

## API Docs

FastAPI auto-generates interactive documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

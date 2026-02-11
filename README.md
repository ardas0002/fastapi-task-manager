# FastAPI Task Manager

A simple task management REST API built with FastAPI and SQLModel. Supports projects and tasks with a one-to-many relationship.

## Tech Stack

- **FastAPI** - web framework
- **SQLModel** - ORM (SQLAlchemy + Pydantic)
- **SQLite** - database
- **Uvicorn** - ASGI server

## Setup

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install -e .
```

## Run

```bash
python -m app.main --reload
```

API will be available at `http://localhost:8000`

## API Endpoints

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects` | Create a new project |
| GET | `/projects` | List projects (with search & pagination) |
| GET | `/projects/{id}` | Get project by ID |
| PUT | `/projects/{id}` | Update project |
| DELETE | `/projects/{id}` | Delete project (tasks get project_id = null) |
| GET | `/projects/{id}/tasks` | List tasks belonging to a project |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a new task (optionally assign to project) |
| GET | `/tasks` | List tasks (with filtering & pagination) |
| GET | `/tasks/{id}` | Get task by ID |
| PUT | `/tasks/{id}` | Update task |
| DELETE | `/tasks/{id}` | Delete task |

### Query Parameters

#### `GET /tasks`

| Parameter | Type | Description |
|-----------|------|-------------|
| `completed` | bool | Filter by completion status |
| `search` | string | Search in title and description |
| `skip` | int | Offset for pagination (default: 0) |
| `limit` | int | Items per page (default: 10, max: 100) |

#### `GET /projects`

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search in name and description |
| `skip` | int | Offset for pagination (default: 0) |
| `limit` | int | Items per page (default: 10, max: 100) |

#### `GET /projects/{id}/tasks`

| Parameter | Type | Description |
|-----------|------|-------------|
| `completed` | bool | Filter by completion status |
| `skip` | int | Offset for pagination (default: 0) |
| `limit` | int | Items per page (default: 10, max: 100) |

## Data Model

```
Project 1 ──── * Task
```

- A **Project** has many **Tasks**
- A **Task** can optionally belong to a **Project** (`project_id`)
- Deleting a project sets `project_id = null` on its tasks (they are not deleted)

## API Docs

FastAPI auto-generates interactive documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

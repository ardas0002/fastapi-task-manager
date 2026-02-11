# FastAPI Task Manager

A task management REST API built with FastAPI and SQLModel. Supports user authentication, projects and tasks with ownership.

## Tech Stack

- **FastAPI** - web framework
- **SQLModel** - ORM (SQLAlchemy + Pydantic)
- **SQLite** - database
- **Uvicorn** - ASGI server
- **python-jose** - JWT tokens
- **passlib + bcrypt** - password hashing

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

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login, returns JWT token |
| GET | `/auth/me` | Get current user info (requires token) |

All endpoints below require `Authorization: Bearer <token>` header.

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/projects` | Create a new project |
| GET | `/projects` | List your projects (with search & pagination) |
| GET | `/projects/{id}` | Get project by ID |
| PUT | `/projects/{id}` | Update project |
| DELETE | `/projects/{id}` | Delete project (tasks get project_id = null) |
| GET | `/projects/{id}/tasks` | List tasks belonging to a project |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/tasks` | Create a new task (optionally assign to project) |
| GET | `/tasks` | List your tasks (with filtering & pagination) |
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

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. Register: `POST /auth/register` with `email`, `username`, `password`
2. Login: `POST /auth/login` with `email`, `password` — returns `access_token`
3. Use the token: add `Authorization: Bearer <token>` header to requests

Tokens expire after 30 minutes.

## Data Model

```
User 1 ──── * Project
User 1 ──── * Task
Project 1 ──── * Task
```

- A **User** owns **Projects** and **Tasks**
- A **Project** has many **Tasks**
- A **Task** can optionally belong to a **Project** (`project_id`)
- Deleting a project sets `project_id = null` on its tasks (they are not deleted)
- Users can only access their own resources (ownership check on all endpoints)

## API Docs

FastAPI auto-generates interactive documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

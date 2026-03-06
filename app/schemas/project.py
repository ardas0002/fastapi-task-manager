from pydantic import BaseModel, Field, ConfigDict
from .task import TaskResponse
from datetime import date

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    priority: int = Field(default= 3, ge=1, le=5)
    due_date: date | None = Field(default=None)

class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=500)
    due_date: date | None = Field(default=None)

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None
    owner_id: int
    due_date: date | None = None
    created: date

class ProjectWithTasksResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None
    due_date: date | None = None
    created: date
    tasks: list[TaskResponse]

class ProjectListResponse(BaseModel):
    projects: list[ProjectResponse]
    total: int
    skip: int
    limit: int

class TaskWithProjectResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    project: ProjectResponse | None


from pydantic import BaseModel, Field, ConfigDict
from .task import TaskResponse

class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=500)

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str | None

class ProjectWithTasksResponse(BaseModel):
    id: int
    name: str
    description: str | None
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


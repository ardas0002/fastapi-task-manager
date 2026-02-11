from pydantic import BaseModel, ConfigDict, Field

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    completed: bool = False
    project_id: int | None = None

class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)"""
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    completed: bool | None = None
    project_id: int | None = None
    

class TaskResponse(BaseModel):
    """Schema for task responses"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    project_id: int | None
    

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    skip: int
    limit: int


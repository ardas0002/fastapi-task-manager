from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = False
    
class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)"""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None
    

class TaskResponse(BaseModel):
    """Schema for task responses"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None
    

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    skip: int
    limit: int
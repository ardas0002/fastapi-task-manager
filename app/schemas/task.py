from pydantic import BaseModel, ConfigDict, Field, field_validator, computed_field
from datetime import date

def validate_future_date(v: date | None) -> date | None:
    if v is not None and v < date.today():
        raise ValueError('Due date must be in future')
    return v

class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    completed: bool = False
    priority: int = Field(default=3, ge=1, le=5)
    due_date: date | None = None
    project_id: int | None = None
    
    @field_validator('due_date')
    @classmethod
    def due_date_in_future(cls, v: date) -> date:
        validate_future_date(v)
    
    @computed_field
    @property
    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return self.due_date < date.today() and not self.completed

class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)"""
    title: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    completed: bool | None = None
    priority: int | None = Field(None, ge=1, le=5)
    due_date: date | None = None
    project_id: int | None = None
    
    @field_validator('due_date')
    @classmethod
    def due_date_in_future(cls, v: date | None) -> date | None:
        validate_future_date(v)
    
    @computed_field
    @property
    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return self.due_date < date.today() and not self.completed

class TaskResponse(BaseModel):
    """Schema for task responses"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    priority: int
    due_date: date | None
    project_id: int | None
    owner_id: int

    @computed_field
    @property
    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return self.due_date < date.today() and not self.completed    

class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int
    skip: int
    limit: int


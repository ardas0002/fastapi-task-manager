from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
from datetime import date

if TYPE_CHECKING:
    from .project import Project
    from .user import User

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    due_date: date | None = Field(default=None)
    priority: int = Field(default=3) 
    project_id: int | None = Field(default=None, foreign_key="project.id", ondelete="SET NULL")
    owner_id: int = Field(foreign_key="user.id")
    is_overdue: bool = Field(default=False)
    owner: "User" = Relationship(back_populates="tasks")
    project: Optional["Project"] = Relationship(back_populates="tasks")

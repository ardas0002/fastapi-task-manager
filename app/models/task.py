from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from .project import Project

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    project_id: int | None = Field(default=None, foreign_key="project.id", ondelete="SET NULL")
    project: Optional["Project"] = Relationship(back_populates="tasks")
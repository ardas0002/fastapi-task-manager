from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task
    from .user import User

class Project(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    owner_id: int = Field(foreign_key="user.id")
    tasks: list["Task"] = Relationship(back_populates="project")
    owner: "User" = Relationship(back_populates="projects")

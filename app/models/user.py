from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from .project import Project
    from .task import Task

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str
    password_hash: str
    is_active: bool = Field(default=True)
  
    projects: list["Project"] = Relationship(back_populates="owner")
    tasks: list["Task"] = Relationship(back_populates="owner")


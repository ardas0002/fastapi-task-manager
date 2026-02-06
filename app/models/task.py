from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
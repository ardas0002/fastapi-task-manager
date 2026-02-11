from fastapi import FastAPI
from app.routers import health, task, project
from app.auth.router import router as auth_router
from app.database import create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API built while learning FastAPI",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(task.router)
app.include_router(project.router)
app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "Welcome to Task Manager API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", reload=True)
from fastapi import FastAPI
from app.routers import health, task, project
from app.auth.router import router as auth_router
from app.database import create_db_and_tables
from app.config import settings
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title=settings.app_name,
    description="A simple task management API",
    version=settings.app_version,
    lifespan=lifespan
)

app.add_middleware(
    SecurityHeadersMiddleware
)

app.add_middleware(
    RequestLoggingMiddleware
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
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
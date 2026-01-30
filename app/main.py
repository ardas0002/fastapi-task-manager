from fastapi import FastAPI 

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API built while learning FastAPI",
    version="0.1.0"
)

fake_db: list[dict] = []
next_id: int = 1

@app.get("/")
def root():
    return {"message": "Welcome to Task Manager API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "0.1.0"}
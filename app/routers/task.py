from fastapi import APIRouter, Query, HTTPException, Depends
from app.schemas import TaskListResponse, TaskResponse, TaskCreate, TaskUpdate
from app.database import get_session
from app.models import Task, Project
from sqlmodel import select, Session

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, session: Session = Depends(get_session)):
    if task_data.project_id is not None:
        if not session.get(Project, task_data.project_id):
            raise HTTPException(404, "Project not found")

    db_task = Task.model_validate(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

@router.get("", response_model=TaskListResponse)
def get_tasks(
    completed: bool | None = None,
    search: str | None = Query(default=None, min_length=1, max_length=60),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    statement = select(Task)
    
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    
    if search:
        statement = statement.where(
            Task.title.contains(search) | Task.description.contains(search)
        )
    
    statement = statement.offset(skip).limit(limit)
    
    tasks = session.exec(statement).all()
    
    count_statement = select(Task)
   
    if completed is not None:
        count_statement = count_statement.where(Task.completed == completed)
    if search:
        count_statement = count_statement.where(
            Task.title.contains(search) | Task.description.contains(search)
            )
    
    total = len(session.exec(count_statement).all())
    
    return TaskListResponse(tasks=tasks, total=total, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    
    if task_update.project_id is not None:
        if not session.get(Project, task_update.project_id):
            raise HTTPException(404, "Project not found")

    update_data = task_update.model_dump(exclude_unset=True)

    task.sqlmodel_update(update_data)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    
    session.delete(task)
    session.commit()
    
    return {"message": "Task deleted"}
from fastapi import APIRouter, Query, HTTPException, Depends
from app.schemas import TaskListResponse, TaskResponse, TaskCreate, TaskUpdate
from app.database import get_session
from app.models import Task 
from sqlmodel import select, Session, select

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task_data: TaskCreate, session: Session = Depends(get_session)) -> TaskResponse:
    db_task = Task.model_validate(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task

@router.get("")
def get_tasks(
    completed: bool | None = None,
    search: str | None = None,
    skip: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    statement = select(Task)
    
    if completed is not None:
        statement = statement.where(Task.completed == completed)
    
    if search:
        statement = statement.where(Task.title.contains(search))
    
    statement = statement.offset(skip).limit(limit)
    
    tasks = session.exec(statement).all()
    
    count_statement = select(Task)
    if completed is not None:
        count_statement = count_statement.where(Task.completed == completed)
    if search:
        count_statement = count_statement.where(Task.title.contains(search))
    
    total = len(session.exec(count_statement).all())
    
    return TaskListResponse(tasks=tasks, total=total, skip=skip, limit=limit)

@router.get("/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)) -> TaskResponse:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return task

@router.put("/{task_id}")
def update_task(task_id: int, task_update: TaskUpdate, session: Session = Depends(get_session)) -> TaskResponse:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    
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
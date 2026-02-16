from fastapi import APIRouter, Query, HTTPException, Depends
from app.schemas import TaskListResponse, TaskResponse, TaskCreate, TaskUpdate
from app.database import get_session
from app.models import Task, Project, User
from app.auth.dependencies import get_current_user
from app.dependencies import get_owned_task
from sqlmodel import select, Session

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if task_data.project_id is not None:
        project = session.get(Project, task_data.project_id)
        if not project:
            raise HTTPException(404, "Project not found")
        if project.owner_id != current_user.id:
            raise HTTPException(403, "Not your project")

    db_task = Task.model_validate(task_data, update={"owner_id": current_user.id})
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
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Task).where(Task.owner_id == current_user.id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    if search:
        statement = statement.where(
            Task.title.contains(search) | Task.description.contains(search)
        )

    statement = statement.offset(skip).limit(limit)

    tasks = session.exec(statement).all()

    count_statement = select(Task).where(Task.owner_id == current_user.id)

    if completed is not None:
        count_statement = count_statement.where(Task.completed == completed)
    if search:
        count_statement = count_statement.where(
            Task.title.contains(search) | Task.description.contains(search)
            )

    total = len(session.exec(count_statement).all())

    return TaskListResponse(tasks=tasks, total=total, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task: Task = Depends(get_owned_task)
):
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_update: TaskUpdate,
    task: Task = Depends(get_owned_task),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if task_update.project_id is not None:
        project = session.get(Project, task_update.project_id)
        if not project:
            raise HTTPException(404, "Project not found")
        if project.owner_id != current_user.id:
            raise HTTPException(403, "Not your project")

    update_data = task_update.model_dump(exclude_unset=True)

    task.sqlmodel_update(update_data)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task

@router.delete("/{task_id}")
def delete_task(
    task: Task = Depends(get_owned_task),
    session: Session = Depends(get_session)
):
    session.delete(task)
    session.commit()

    return {"message": "Task deleted"}

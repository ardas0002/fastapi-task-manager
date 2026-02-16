from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from app.database import get_session
from app.dependencies import get_owned_project
from app.models import Project, Task, User
from app.auth.dependencies import get_current_user
from app.schemas import *


router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    project_data: ProjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_project = Project.model_validate(project_data, update={"owner_id": current_user.id})
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@router.get("", response_model=ProjectListResponse)
def get_projects(
    search: str | None = Query(default=None, min_length=1, max_length=60),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Project).where(Project.owner_id == current_user.id)

    if search:
        statement = statement.where(
            Project.name.contains(search) | Project.description.contains(search)
        )

    statement = statement.offset(skip).limit(limit)

    projects = session.exec(statement).all()

    count_statement = select(Project).where(Project.owner_id == current_user.id)

    if search:
        count_statement = count_statement.where(
            Project.name.contains(search) | Project.description.contains(search)
        )

    total = len(session.exec(count_statement).all())

    return ProjectListResponse(projects=projects, total=total, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project: Project = Depends(get_owned_project)
):
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_update: ProjectUpdate,
    project: Project = Depends(get_owned_project),
    session: Session = Depends(get_session),
):   
    update_data = project_update.model_dump(exclude_unset=True)

    project.sqlmodel_update(update_data)

    session.add(project)
    session.commit()
    session.refresh(project)

    return project

@router.delete("/{project_id}")
def delete_project(
    project: Project = Depends(get_owned_project),
    session: Session = Depends(get_session)
) -> dict:
    session.delete(project)
    session.commit()

    return {"message": "Project deleted"}

@router.get("/{project_id}/tasks", response_model=TaskListResponse)
def get_project_tasks(
    completed: bool | None = None,
    project: Project = Depends(get_owned_project),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    statement = select(Task).where(Task.project_id == project.id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    statement = statement.offset(skip).limit(limit)

    tasks = session.exec(statement).all()

    count_statement = select(Task).where(Task.project_id == project.id)

    if completed is not None:
        count_statement = count_statement.where(Task.completed == completed)

    total = len(session.exec(count_statement).all())

    return TaskListResponse(tasks=tasks, total=total, skip=skip, limit=limit)

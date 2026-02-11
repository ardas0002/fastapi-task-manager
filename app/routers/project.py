from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import Project, Task
from app.schemas import *

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(project_data: ProjectCreate, session: Session = Depends(get_session)):
    db_project = Project.model_validate(project_data)
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

@router.get("", response_model=ProjectListResponse)
def get_projects(
    search: str | None = Query(default=None, min_length=1, max_length=60),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    statement = select(Project)

    if search:
        statement = statement.where(
            Project.name.contains(search) | Project.description.contains(search)
        )

    statement = statement.offset(skip).limit(limit)

    projects = session.exec(statement).all()

    count_statement = select(Project)

    if search:
        count_statement = count_statement.where(
            Project.name.contains(search) | Project.description.contains(search)
        )

    total = len(session.exec(count_statement).all())

    return ProjectListResponse(projects=projects, total=total, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectUpdate, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    
    update_data = project_update.model_dump(exclude_unset=True)

    project.sqlmodel_update(update_data)

    session.add(project)
    session.commit()
    session.refresh(project)

    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, session: Session = Depends(get_session)):
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    session.delete(project)
    session.commit()

    return {"message": "Project deleted"}

@router.get("/{project_id}/tasks", response_model=TaskListResponse)
def get_project_tasks(
    project_id: int,
    completed: bool | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """Pobierz taski należące do projektu"""
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")

    statement = select(Task).where(Task.project_id == project_id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    statement = statement.offset(skip).limit(limit)

    tasks = session.exec(statement).all()

    count_statement = select(Task).where(Task.project_id == project_id)

    if completed is not None:
        count_statement = count_statement.where(Task.completed == completed)

    total = len(session.exec(count_statement).all())

    return TaskListResponse(tasks=tasks, total=total, skip=skip, limit=limit)


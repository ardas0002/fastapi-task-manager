from app.models import Task, Project
from app.database import get_session
from app.models import User
from app.auth import get_current_user
from fastapi import Depends
from sqlmodel import Session
from fastapi import HTTPException


def get_owned_task(task_id: int,
                  session: Session = Depends(get_session),
                  current_user: User = Depends(get_current_user)) -> Task:

    task = session.get(Task, int(task_id))

    if task is None:
        raise HTTPException(
            status_code=404, 
            detail="Task not found"
        )
    
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this task"
        )
    
    return task

def get_owned_project(project_id: int,
                      session: Session = Depends(get_session),
                      current_user: User = Depends(get_current_user)) -> Project:
    
    
    project = session.get(Project, int(project_id))

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You don't have access to this project"
        )
    
    return project
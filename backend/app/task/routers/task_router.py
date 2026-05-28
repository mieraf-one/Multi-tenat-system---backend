from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.user.models import User
from app.task.schemas import TaskIn, TaskOut, TaskUpdate
from app.task.services import create_task, get_all_tasks, update_task, delete_task



router = APIRouter(
    prefix='/projects',
    tags=['Tasks']
)


@router.post('/{project_id}/tasks', response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task_route(
        data: TaskIn,
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

    return create_task(data, project_id, db)




@router.get('/{project_id}/tasks', response_model=List[TaskOut])
def get_all_tasks_route(
        project_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

    return get_all_tasks(project_id, current_user.id, db)



@router.patch('/{project_id}/tasks/{task_id}', response_model=TaskOut)
def update_task_route(
        data: TaskUpdate,
        project_id: int,
        task_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

    return update_task(data, task_id, project_id, current_user.id, db)



@router.delete('/{project_id}/tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def update_task_route(
        project_id: int,
        task_id: int,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

    return delete_task(task_id, current_user.id, project_id, db)

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.task.schemas import TaskUpdate
from app.task.services import validate_permission
from app.task.models import Task




def validate_task(task_id: int, user_id: int, project_id: int, db: Session):
    task = (
        db.query(Task)
            .filter(Task.id == task_id)
            .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    
    if task.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task is not in this Project'
        )
    
    validate_permission(task.tenant_id, user_id, db)

    return task



def update(task: Task, data: TaskUpdate):
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    return task



def save_task(task: Task, db: Session):
    try:
        db.commit()
        db.refresh(task)

        return task
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='something went wrong'
        )




def update_task(data: TaskUpdate, task_id: int, project_id: int, user_id: int, db: Session):
    task = validate_task(task_id, user_id, project_id, db)
    updated = update(task, data)
    return save_task(updated, db)
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.task.schemas import TaskIn
from app.task.models import Task
from app.task.services import validate_permission



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


def save_task(task: Task, db: Session):
    try:
        db.delete(task)
        db.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='something went wrong'
        )


def delete_task(task_id: int, user_id: int, project_id: int, db: Session):
    task = validate_task(task_id, user_id, project_id, db)
    save_task(task, db)

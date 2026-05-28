from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.task.schemas import TaskIn
from app.task.models import Task

    

def save_task(task: Task, db: Session):
    try:
        db.add(task)
        db.commit()
        db.refresh(task)

        return task
    except Exception:
        db.rollback()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='something went wrong'
        )

def validate_task_uniqueness(task_title: str, project_id: int, db: Session):
    task = (
        db.query(Task)
            .filter(
                Task.title == task_title,
                Task.project_id == project_id)
            .first()
    )

    if task is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Task name already used'
        )
    


def create_task(data: TaskIn, project_id: int, db: Session):
    # validate task title is unique
    validate_task_uniqueness(data.title, project_id, db)

    # create new task
    new_task = Task(
        title=data.title,
        content=data.content,
        project_id=project_id,
        tenant_id=data.tenant_id
    )

    # save and return new task
    return save_task(new_task, db)
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.project.models import Project


def get_project(project_id: int, tenant_id: int, db: Session):
    project = (
        db.query(Project)
            .filter(
                Project.id == project_id,
                Project.tenant_id == tenant_id)
            .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project not found'
        )

    return project

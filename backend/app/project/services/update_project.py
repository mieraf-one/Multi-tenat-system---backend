from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.project.models import Project
from app.project.schemas import ProjectUpdate



def validate_project(project_id: int, tenant_id: int, db: Session):
    project = (
        db.query(Project)
            .filter(
                Project.id == project_id,
                Project.tenant_id == tenant_id)
            .first()
    )

    if project is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail='Project not found'
        )
    
    return project


def validate_project_name_uniqueness(new_name: str, project_id: int, tenant_id: int, db: Session):
    project = (
        db.query(Project)
            .filter(
                Project.tenant_id == tenant_id,
                Project.id != project_id,
                Project.name == new_name)
            .first()
    )


    if project is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Project name already used'
        )
    



def update_project(data: ProjectUpdate, project_id: int, tenant_id: int, db: Session):
    # validate project existance
    project = validate_project(project_id, tenant_id, db)

    # validate new name uniqueness
    validate_project_name_uniqueness(data.name, project_id, tenant_id, db)

    # update name
    project.name = data.name

    try:
        db.commit()
        db.refresh(project)

        return project
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='something went wrong'
        )
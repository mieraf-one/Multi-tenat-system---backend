from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.project.schemas import ProjectIn
from app.project.models import Project
from app.tenant.models import Tenant




def validate_project_name_uniqueness(name: str, tenant_id: int, db: Session):
    project = (
        db.query(Project)
            .filter(
                Project.name == name,
                Project.tenant_id == tenant_id
            )
            .first()
    )

    if project is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Project name already used'
        )
    

def validate_tenant_existence(tenant_id: int, db: Session):
    tenant = (
        db.query(Tenant)
            .filter(Tenant.id == tenant_id)
            .first()
    )

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tenant not found'
        )


def save_project(project: Project, db: Session):
    try:
        db.add(project)
        db.commit()
        db.refresh(project)

        return project
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='something went wrong'
        )




def create_project(data: ProjectIn, db: Session):
    # validate project name is unique
    validate_project_name_uniqueness(data.name, data.tenant_id, db)

    # validate tenant existance
    validate_tenant_existence(data.tenant_id, db)

    # create new Project
    new_project = Project(
        name=data.name,
        tenant_id=data.tenant_id
    )

    # save the new project
    return save_project(new_project, db)

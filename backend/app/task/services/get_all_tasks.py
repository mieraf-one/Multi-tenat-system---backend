from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.project.models import Project
from app.tenant.models import TenantMember

    

def validate_permission(tenant_id: int, user_id: int, db: Session):
    tenant_member = (
        db.query(TenantMember)
            .filter(
                TenantMember.user_id == user_id,
                TenantMember.tenant_id == tenant_id)
            .first()
    )

    if tenant_member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not allowed to see this tasks'
        )




def get_all_tasks(project_id: int, user_id: int, db: Session):
    project = (
        db.query(Project)
            .options(joinedload(Project.tasks))
            .filter(Project.id == project_id)
            .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project not found'
        )

    # validate user permission
    validate_permission(project.tenant_id, user_id, db)

    return project.tasks

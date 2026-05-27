from fastapi import HTTPException,status
from sqlalchemy.orm import Session

from app.project.models import Project
from app.tenant.models import TenantMember, RoleEnum


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
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Project not found'
        )   
    
    return project

    

def check_permission(user_id: int, tenant_id: int, db: Session):
    member = (
        db.query(TenantMember)
            .filter(
                TenantMember.user_id == user_id,
                TenantMember.tenant_id == tenant_id)
            .first()
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You are not a member of this tenant'
        )
    
    if member.role not in [RoleEnum.OWNER, RoleEnum.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this project"
        )


def save_delete(project: Project, db: Session):
    try:
        db.delete(project)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="something went wrong"
        )



def delete_project(user_id: int, project_id: int, tenant_id: int, db: Session):
    # validate project existance
    project = validate_project(project_id, tenant_id, db)

    # validate permission
    check_permission(user_id, tenant_id, db)

    # delete project
    save_delete(project, db)

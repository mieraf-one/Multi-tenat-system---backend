from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.tenant.models import TenantMember, Tenant


def get_tenant(user_id: int, tenant_id: int, db: Session) -> Tenant:
    member = (
        db.query(TenantMember)
            .options(joinedload(TenantMember.tenant))
            .filter(
                TenantMember.user_id == user_id,
                TenantMember.tenant_id == tenant_id)
            .first()

    )
    
    # check tenant existance
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Tenant not found'
        )
    
    return member.tenant

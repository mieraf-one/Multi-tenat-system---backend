from sqlalchemy.orm import Session, joinedload

from app.tenant.models import TenantMember


def get_all_tenants(user_id: int, db: Session):
    members = (
        db.query(TenantMember)
            .options(joinedload(TenantMember.tenant))
            .filter(TenantMember.user_id == user_id)
            .all()
    )
    
    
    return [member.tenant for member in members]
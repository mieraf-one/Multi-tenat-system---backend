from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.tenant.schemas import TenantIn
from app.tenant.models import Tenant, TenantMember, RoleEnum



def validate_slug_uniqueness(slug: str, db: Session):
    tenant = db.query(Tenant).filter(Tenant.slug==slug).first()

    if tenant is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Slug already used'
        )



def create_new_tenant(data: TenantIn, user_id: int, db: Session):
    # validate if slug is unique
    validate_slug_uniqueness(data.slug, db)

    try:
        # create new tenant
        new_tenant = Tenant(
            name=data.name,
            slug=data.slug
        )

        db.add(new_tenant)
        db.flush() # temporary save in db

        
        # gather new tenant member data
        new_tenant_member = TenantMember(
            user_id=user_id,
            tenant_id=new_tenant.id,
            role=RoleEnum.OWNER
        )

        # create new tenant member 
        db.add(new_tenant_member)

        db.commit()
        db.refresh(new_tenant)

        return new_tenant
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Something went wrong'
        )
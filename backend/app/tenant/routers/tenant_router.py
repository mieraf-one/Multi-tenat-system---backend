from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.user.models import User
from app.core.database import get_db
from app.tenant.schemas import TenantIn, TenantOut
from app.dependencies.auth import get_current_user
from app.tenant.services import create_new_tenant, get_all_tenants, get_tenant




router = APIRouter(
    prefix='/tenants',
    tags=['Tenant']
)



# ------------------------------------------------
#                 CREATE TENANT
# ------------------------------------------------
@router.post('/register', response_model=TenantOut, status_code=status.HTTP_201_CREATED)
def create_tenant_route(data: TenantIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_new_tenant(data, current_user.id, db)


# ------------------------------------------------
#                 GET ALL TENANTS
# ------------------------------------------------
@router.get('/me', response_model=List[TenantOut])
def get_all_tenants_route(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_all_tenants(current_user.id, db)



# ------------------------------------------------
#                 GET TENANT
# ------------------------------------------------
@router.get('/{id}/me', response_model=TenantOut)
def get_tenant_route(id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_tenant(current_user.id, tenant_id=id, db=db)
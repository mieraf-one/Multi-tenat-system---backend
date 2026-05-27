from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.project.services import (
        create_project, get_all_projects,
        get_project, update_project, delete_project
    )

from app.project.schemas import ProjectIn, ProjectOut, ProjectUpdate
from app.user.models import User
from app.dependencies.auth import get_current_user
from app.core.database import get_db




router = APIRouter(
    prefix='/projects',
    tags=['Projects']
)

# -----------------------------------------
#               CREATE PROJECT
# -----------------------------------------
@router.post('/', response_model=ProjectOut)
def create_project_route(data: ProjectIn, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_project(data, db)


# -----------------------------------------
#         GET ALL PROJECTS IN A TENANT
# -----------------------------------------
@router.get('/{tenant_id}/tenant', response_model=List[ProjectOut])
def get_all_projects_route(tenant_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_all_projects(tenant_id, db)


# -----------------------------------------
#           GET A PROJECT IN A TENANT
# -----------------------------------------
@router.get('/{project_id}/tenant/{tenant_id}', response_model=ProjectOut)
def get_project_route(project_id: int, tenant_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_project(project_id, tenant_id, db)



# -----------------------------------------
#           UPDATE A PROJECT IN A TENANT
# -----------------------------------------
@router.patch('/{project_id}/tenant/{tenant_id}', response_model=ProjectOut)
def update_project_route(data: ProjectUpdate, project_id: int, tenant_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return update_project(data, project_id, tenant_id, db)




# -----------------------------------------
#           DELETE A PROJECT IN A TENANT
# -----------------------------------------
@router.delete('/{project_id}/tenant/{tenant_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_project_route(project_id: int, tenant_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return delete_project(current_user.id, project_id, tenant_id, db)

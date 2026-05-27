from sqlalchemy.orm import Session

from app.project.models import Project


def get_all_projects(tenant_id: int, db: Session):
    projects = (
        db.query(Project)
            .filter(Project.tenant_id == tenant_id)
            .all()
    )

    return projects
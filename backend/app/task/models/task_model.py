from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base



def get_now():
    return datetime.now(timezone.utc)



class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)

    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)

    updated_at = Column(DateTime(timezone=True), default=get_now, onupdate=get_now)
    created_at = Column(DateTime(timezone=True), default=get_now)

    project = relationship(
        'Project',
        back_populates='tasks'
    )

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    tenant_id = Column(Integer, ForeignKey('tenants.id'), nullable=False)

    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    tenant = relationship(
        'Tenant',
        back_populates='projects'
    )

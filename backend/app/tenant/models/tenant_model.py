from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

import enum
from datetime import datetime, timezone

from app.core.database import Base
from app.tenant.models import tenant_model



class Tenant(Base):
    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True)
    api_key = Column(String, nullable=True)

    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    tenant_members = relationship(
        "TenantMember",
        back_populates="tenant"
    )



class RoleEnum(str, enum.Enum):
    OWNER = 'owner'
    ADMIN = 'admin'
    USER = 'user'



class TenantMember(Base):
    __tablename__ = 'tenant_members'

    # User FK
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True, nullable=False)
    
    # Tenant FK
    tenant_id = Column(Integer, ForeignKey('tenants.id'), primary_key=True, nullable=False)

    # User role
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)

    # created at
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # relationships
    user = relationship(
        "User",
        back_populates="tenant_members"
    )

    tenant = relationship(
        "Tenant",
        back_populates="tenant_members"
    )

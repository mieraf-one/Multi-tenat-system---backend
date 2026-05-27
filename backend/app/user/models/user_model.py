from sqlalchemy import Column, Integer, String, Boolean, DateTime, desc
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.core.database import Base
from app.user.models import token_model
from app.user.models.verification_code_model import EmailVerificationCode
from app.tenant.models import TenantMember


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String,unique=True, nullable=True, index=True)

    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)


    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    refresh_tokens = relationship(
        'RefreshToken',
        back_populates='user',
        cascade="all, delete-orphan"
    )

    sent_codes = relationship(
        'EmailVerificationCode',
        back_populates='user',
        order_by=lambda: desc(EmailVerificationCode.created_at)
    )


    tenant_members = relationship(
        "TenantMember",
        back_populates="user"
    )

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProjectIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    tenant_id: int



class ProjectOut(BaseModel):
    id: int
    name: str
    tenant_id: int
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
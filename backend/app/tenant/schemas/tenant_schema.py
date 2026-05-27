from datetime import datetime
from typing import Optional

from pydantic import BaseModel



class TenantIn(BaseModel):
    name: str
    slug: str


class TenantOut(BaseModel):
    id: int
    name: str
    slug: str
    api_key: Optional[str] = None
    updated_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

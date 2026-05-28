from pydantic import BaseModel, Field



class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    content: str | None = Field(default=None, min_length=1)
    tenant_id: int

class TaskOut(BaseModel):
    id: int
    project_id: int
    tenant_id: int
    title: str
    content: str | None


    class Config:
        from_attributes = True


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    content: str | None = Field(default=None, min_length=1)

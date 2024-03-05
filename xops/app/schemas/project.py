from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass

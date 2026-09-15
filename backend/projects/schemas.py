from pydantic import BaseModel, Field

# 1. Base schema (fields shared by all project schemas)
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None

# 2. Schema for creating a project (Input)
class ProjectCreate(ProjectBase):
    pass

# 3. Schema for returning project data (Output)
class ProjectResponse(ProjectBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}
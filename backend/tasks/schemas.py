from pydantic import BaseModel, Field
from tasks.models import TaskStatus

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO

class TaskCreate(TaskBase):
    project_id: int

class TaskResponse(TaskBase):
    id: int
    project_id: int
    assignee_id: int | None = None

    model_config = {"from_attributes": True}
from datetime import datetime
from pydantic import BaseModel, Field

# Input Schema
class CommentCreate(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)

# Output Schema
class CommentResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    task_id: int
    user_id: int

    model_config = {"from_attributes": True}
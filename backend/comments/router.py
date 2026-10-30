from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from comments.models import Comment
from comments.schemas import CommentCreate, CommentResponse
from tasks.models import Task
from projects.models import Project
from users.models import User
from users.router import get_current_user

router = APIRouter(prefix="/tasks/{task_id}/comments", tags=["Comments"])

def verify_task_access(task_id: int, user_id: int, db: Session) -> Task:
    """Helper to verify that the task exists and belongs to a project owned by the user."""
    task = db.query(Task).join(Project).filter(
        Task.id == task_id,
        Project.owner_id == user_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found or access denied"
        )
    return task

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    task_id: int,
    comment_in: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Verify user owns the project this task belongs to
    verify_task_access(task_id, current_user.id, db)

    # 2. Create the comment linked to task and user
    new_comment = Comment(
        text=comment_in.text.strip(),
        task_id=task_id,
        user_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/", response_model=list[CommentResponse])
def list_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Verify user owns the project this task belongs to
    verify_task_access(task_id, current_user.id, db)

    # 2. Return all comments on this task, ordered by oldest to newest
    return db.query(Comment).filter(
        Comment.task_id == task_id
    ).order_by(Comment.created_at.asc()).all()
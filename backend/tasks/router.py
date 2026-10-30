from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from tasks.models import Task, TaskStatus
from tasks.schemas import TaskCreate, TaskResponse, TaskUpdateStatus
from users.router import get_current_user
from users.models import User
from sqlalchemy import or_  # Needed for searching in title OR description


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

     # Check if project exists
    from projects.models import Project # Import here to avoid circular imports
    project = db.query(Project).filter(Project.id == task_in.project_id,Project.owner_id == current_user.id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found or you are not authorized to add tasks to it")

    new_task = Task(**task_in.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=list[TaskResponse])
def list_tasks(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user),
                status: TaskStatus | None = None,
                search: str | None = None,
                skip: int = Query(0, ge=0),          # ge=0 means 'greater than or equal to 0'
                limit: int = Query(20, ge=1, le=100),):
   # 1. First, verify the project actually exists AND belongs to the user
    from projects.models import Project
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to access this project's tasks")
    
    # 1. Base query: must belong to the project AND the current user
    query = db.query(Task).filter(
        Task.project_id == project_id
    )

    # 2. Optional Filter: by status (if provided)
    if status:
        query = query.filter(Task.status == status)

    # 3. Optional Search: case-insensitive search in title OR description
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            )
        )

    # 4. Pagination: apply offset and limit, then execute query
    tasks = query.offset(skip).limit(limit).all()
    return tasks

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Fetch task and ensure the project it belongs to is owned by the current_user
    from projects.models import Project
    task = db.query(Task).join(Project).filter(Task.id == task_id, Project.owner_id == current_user.id).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")
        
    db.delete(task)
    db.commit()
    return None


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    task_update: TaskUpdateStatus,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from projects.models import Project

    # Verify task exists AND belongs to a project owned by the current user
    task = db.query(Task).join(Project).filter(
        Task.id == task_id,
        Project.owner_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")

    # Update the status and commit
    task.status = task_update.status
    db.commit()
    db.refresh(task)
    return task
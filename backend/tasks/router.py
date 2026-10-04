from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from tasks.models import Task
from tasks.schemas import TaskCreate, TaskResponse
from users.router import get_current_user
from users.models import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

     # Check if project exists
    from projects.models import Project # Import here to avoid circular imports
    project = db.query(Project).filter(Project.id == task_in.project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    new_task = Task(**task_in.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.get("/", response_model=list[TaskResponse])
def list_tasks(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
   # 1. First, verify the project actually exists AND belongs to the user
    from projects.models import Project
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to access this project's tasks")
    
    # 2. Now it is safe to return the tasks
    return db.query(Task).filter(Task.project_id == project_id).all()

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
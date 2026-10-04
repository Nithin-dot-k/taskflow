from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from projects.models import Project
from projects.schemas import ProjectCreate, ProjectResponse
from users.router import get_current_user # We will implement this next!
from users.models import User

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_project = Project(**project_in.model_dump(), owner_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    return projects

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Fetch the project and verify ownership
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # 2. Delete it
    db.delete(project)
    db.commit()
    return None
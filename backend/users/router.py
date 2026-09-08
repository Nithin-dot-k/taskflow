from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from users.models import User
from users.schemas import UserCreate, UserResponse
from users.utils import hash_password

# 1. Initialize the router with a prefix and tags for organization
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if a user with this email already exists in the database
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )

    # 2. Encrypt (hash) their plain text password
    hashed_pw = hash_password(user_in.password)

    # 3. Create a new User database object and save it
    new_user = User(email=user_in.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # This fetches the newly generated database ID for us

    # 4. Return the new user (FastAPI will automatically filter this into UserResponse!)
    return new_user
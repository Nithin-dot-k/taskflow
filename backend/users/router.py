from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from users.models import User
from users.schemas import UserCreate, UserResponse, Token 
from users.schemas import UserCreate, UserResponse
from users.utils import hash_password, verify_password, create_access_token
from fastapi.security import OAuth2PasswordBearer
import jwt
from config import settings

# 1. Initialize the router with a prefix and tags for organization
router = APIRouter(prefix="/auth", tags=["Authentication"])

# This tells FastAPI where to look for the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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

# --- LOGIN ENDPOINT ---
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # 2. Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    # 3. Return the token
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decode the token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Get user from DB
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
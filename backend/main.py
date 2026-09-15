from fastapi import FastAPI
from config import settings
from database import Base, engine
from users.router import router as auth_router  # Import our new router
from projects.models import Project 

Base.metadata.create_all(bind=engine)

# Tell SQLAlchemy to create all tables in our database (if they don't exist yet)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Register our authentication router with the app
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}!"}
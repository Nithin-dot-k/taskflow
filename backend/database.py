from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from config import settings

# 1. Create the Engine (The physical connection pipeline)
engine = create_engine(settings.DATABASE_URL)

# 2. Create SessionLocal (The factory for database sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Create the Base Class (The master blueprint for our tables)
class Base(DeclarativeBase):
    pass

# 4. Create the Database Session Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
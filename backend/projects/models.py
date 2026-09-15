from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Use string "User" to avoid circular imports
    owner = relationship("User", back_populates="projects")
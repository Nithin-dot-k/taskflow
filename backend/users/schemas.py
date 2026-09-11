from pydantic import BaseModel, EmailStr, Field

# 1. Base schema for shared fields
class UserBase(BaseModel):
    email: EmailStr

# 2. Schema for incoming registration data (Input Validation)
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

# 3. Schema for returning user data (Output Filtering)
class UserResponse(UserBase):
    id: int

    # This tells Pydantic to read SQLAlchemy model objects as if they were simple dictionaries
    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
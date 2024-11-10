"""Module to define Pydantic schemas for models used"""
from typing import Optional
from pydantic import BaseModel, EmailStr


class BookBase(BaseModel):
    """Pydantic schema for Book model"""
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None  # Optional summary

class BookCreate(BookBase):
    """Pydantic schema for Book Create model"""

class BookResponse(BookBase):
    """Pydantic schema for Book Response model"""
    id: int

    class Config:
        orm_mode = True  # Allows SQLAlchemy models to be used with Pydantic

class BookUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year_published: Optional[int] = None
    # Add other fields if needed

    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    """Pydantic schema for Review model"""
    rating: float
    review_text: Optional[str] = None

class ReviewCreate(ReviewBase):
    """Pydantic schema for Review Create model"""

class ReviewResponse(ReviewBase):
    """Pydantic schema for Review Response model"""
    id: int
    book_id: int
    user_id: int

    class Config:
        orm_mode = True

# Pydantic schema for User model
class UserBase(BaseModel):
    """Pydantic schema for User model"""
    username: str
    email: str
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    """Pydantic schema for User Create model"""
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """Pydantic schema for User Login model"""
    username: str
    password: str

class Token(BaseModel):
    """Pydantic schema for Token model"""
    access_token: str
    token_type: str

class UserResponse(UserBase):
    """Pydantic schema for User Response model"""

class SummaryRequest(BaseModel):
    """Pydantic schema for Summary Request (for generating summaries)"""
    content: str  # The content of the book to be summarized


class SummaryResponse(BaseModel):
    """Pydantic schema for Summary Response (response after generating the summary)"""
    summary: str  # The generated summary text

    class Config:
        orm_mode = True

class RecommendationRequest(BaseModel):
    """Pydantic schema for Recommendation request"""
    content: str # The content of the user's request to recommend

class RecommendationResponse(BaseModel):
    """Pydantic schema for Recommendation response"""
    recommendation: list[str] # The list of recommendations

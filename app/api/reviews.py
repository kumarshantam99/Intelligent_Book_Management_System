"""Module to define reviews routes"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Review, Book
from app.schemas import ReviewCreate, ReviewResponse
from app.database import get_db
from app.auth import get_current_user


router = APIRouter()


@router.post("/{book_id}", response_model=ReviewResponse)
async def create_review(book_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Add a review for a book"""
    db_book = await db.execute(select(Book).filter(Book.id == book_id))
    db_book = db_book.scalars().first()
    
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_review = Review(book_id=book_id, user_id=user_id,  **review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

@router.get("/{book_id}", response_model=List[ReviewResponse])
async def get_reviews(book_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Get a review for a book"""
    db_book = await db.execute(select(Book).filter(Book.id == book_id))
    db_book = db_book.scalars().first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    result = await db.execute(select(Review).filter(Review.book_id == book_id))
    reviews = result.scalars().all()
    return reviews

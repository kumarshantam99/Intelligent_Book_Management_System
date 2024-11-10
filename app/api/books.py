"""Module to handle book routes"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Book, Review
from app.schemas import BookCreate, BookResponse, BookUpdate
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=BookResponse)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Create book entry"""
    db_book = Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.get("/", response_model=List[BookResponse])
async def get_books(db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Get all books"""
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Get book using book id"""
    db_book = await db.execute(select(Book).filter(Book.id == book_id))
    db_book = db_book.scalars().first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book: BookUpdate, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Update current book"""
    db_book = await db.execute(select(Book).filter(Book.id == book_id))
    db_book = db_book.scalars().first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", response_model=BookResponse)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Delete current book"""
    db_book = await db.execute(select(Book).filter(Book.id == book_id))
    db_book = db_book.scalars().first()
    
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await db.delete(db_book)
    await db.commit()
    return db_book

@router.get("/{book_id}/summary")
async def get_book_summary(book_id: int, db: AsyncSession = Depends(get_db), user_id: int = Depends(get_current_user)):
    """Fetch the book from the database"""
    db_book = await db.execute(select(Book).filter(Book.id == book_id))
    db_book = db_book.scalars().first()

    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Retrieve all reviews for the book
    result = await db.execute(select(Review).filter(Review.book_id == book_id))
    reviews = result.scalars().all()

    # Calculate the aggregated rating
    if reviews:
        avg_rating = sum([review.rating for review in reviews]) / len(reviews)
    else:
        avg_rating = 0

    # Return the book's summary and the aggregated rating
    return {
        "book_id": db_book.id,
        "title": db_book.title,
        "author": db_book.author,
        "summary": db_book.summary,  # Fetch the summary from the book column
        "average_rating": avg_rating
    }

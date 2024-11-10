from fastapi import APIRouter, Depends, HTTPException
from app.services.recommendation_engine import recommend_books
from app.auth import get_current_user
from app.schemas import RecommendationRequest, RecommendationResponse
from app.database import get_db
from app.models import Book
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


router = APIRouter()

async def get_all_books(db: AsyncSession):
    """Get all books"""
    result = await db.execute(select(Book))
    books = result.scalars().all()
    return books

@router.get("/", response_model=RecommendationResponse)
async def generate_recommendations(request: RecommendationRequest, db: AsyncSession = Depends(get_db), current_user: str = Depends(get_current_user)):
    """Calling llama_service"""
    try:
        books = await get_all_books(db)
        recommendation = recommend_books(request.content, books)
        return {"recommendation": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching recommendations: {e}") from e

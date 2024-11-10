"""Summary endpoint definiton"""
from fastapi import APIRouter, Depends, HTTPException
from app.services.llama_service import llama_service
from app.auth import get_current_user
from app.schemas import SummaryRequest, SummaryResponse

router = APIRouter()

@router.post("/generate-summary", response_model=SummaryResponse)
async def generate_summary(request: SummaryRequest, current_user: str = Depends(get_current_user)):
    """Calling llama_service"""
    try:
        summary = await llama_service.generate_summary(request.content)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {e}") from e

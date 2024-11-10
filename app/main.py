# app/main.py
from fastapi import FastAPI
from app.api import books, reviews, recommendations, summaries, auth
from app.database import engine
from app.models import Base

app = FastAPI()

# Include Routers
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])
app.include_router(summaries.router, prefix="/summaries", tags=["Summaries"])

# Create the database tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

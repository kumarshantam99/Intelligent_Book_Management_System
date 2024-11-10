import pytest
from unittest.mock import Mock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.models import Book
from app.schemas import RecommendationRequest, RecommendationResponse

# Test data
mock_books = [
    Book(id=1, title="Book 1", author="Author 1"),
    Book(id=2, title="Book 2", author="Author 2")
]

mock_recommendation = "Based on your interests, you might enjoy Book 1 and Book 2."

@pytest.fixture
def mock_db():
    """Fixture for mocking database session"""
    async def mock_execute(query):
        class MockResult:
            def scalars(self):
                return self
            def all(self):
                return mock_books
        return MockResult()
    
    session = Mock(spec=AsyncSession)
    session.execute = mock_execute
    return session

@pytest.fixture
def mock_user():
    """Fixture for mocking authenticated user"""
    return "test_user"

@pytest.mark.asyncio
async def test_get_all_books_success():
    """Test successful retrieval of all books"""
    db = await mock_db()
    books = await get_all_books(db)
    
    assert len(books) == 2
    assert books == mock_books
    assert books[0].title == "Book 1"
    assert books[1].title == "Book 2"

@pytest.mark.asyncio
async def test_generate_recommendations_success():
    """Test successful generation of book recommendations"""
    with patch('app.services.recommendation_engine.recommend_books', return_value=mock_recommendation):
        db = await mock_db()
        request = RecommendationRequest(content="I like science fiction")
        
        response = await generate_recommendations(request, db, "test_user")
        
        assert isinstance(response, dict)
        assert response["recommendation"] == mock_recommendation

@pytest.mark.asyncio
async def test_generate_recommendations_database_error():
    """Test handling of database errors"""
    async def mock_execute_error(query):
        raise Exception("Database connection error")
    
    db = Mock(spec=AsyncSession)
    db.execute = mock_execute_error
    
    request = RecommendationRequest(content="I like science fiction")
    
    with pytest.raises(HTTPException) as exc_info:
        await generate_recommendations(request, db, "test_user")
    
    assert exc_info.value.status_code == 500
    assert "Error fetching recommendations" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_generate_recommendations_recommendation_error():
    """Test handling of recommendation engine errors"""
    db = await mock_db()
    request = RecommendationRequest(content="I like science fiction")
    
    with patch('app.services.recommendation_engine.recommend_books', side_effect=Exception("Recommendation engine error")):
        with pytest.raises(HTTPException) as exc_info:
            await generate_recommendations(request, db, "test_user")
        
        assert exc_info.value.status_code == 500
        assert "Error fetching recommendations" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_generate_recommendations_empty_content():
    """Test handling of empty content in request"""
    db = await mock_db()
    request = RecommendationRequest(content="")
    
    with patch('app.services.recommendation_engine.recommend_books', return_value=mock_recommendation):
        response = await generate_recommendations(request, db, "test_user")
        assert isinstance(response, dict)
        assert response["recommendation"] == mock_recommendation

# Parameterized test for different content inputs
@pytest.mark.asyncio
@pytest.mark.parametrize("content,expected", [
    ("I like science fiction", mock_recommendation),
    ("Fantasy books", mock_recommendation),
    ("Mystery novels", mock_recommendation),
])
async def test_generate_recommendations_different_contents(content, expected):
    """Test recommendations with different content inputs"""
    with patch('app.services.recommendation_engine.recommend_books', return_value=expected):
        db = await mock_db()
        request = RecommendationRequest(content=content)
        
        response = await generate_recommendations(request, db, "test_user")
        
        assert isinstance(response, dict)
        assert response["recommendation"] == expected
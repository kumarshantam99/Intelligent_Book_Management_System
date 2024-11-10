import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock, patch
from app.models import Book, Review
from app.schemas import BookCreate
from app.database import get_db
from app.auth import get_current_user

# Test data
test_book = {
    "title": "Test Book",
    "author": "Test Author",
    "summary": "Test Summary"
}

@pytest.fixture
async def app():
    app = FastAPI()
    app.include_router(router)
    return app

@pytest.fixture
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def mock_db():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
async def mock_current_user():
    return 1

# Override dependencies
@pytest.fixture(autouse=True)
async def override_dependencies(app, mock_db, mock_current_user):
    app.dependency_overrides[get_db] = lambda: mock_db
    app.dependency_overrides[get_current_user] = lambda: mock_current_user
    yield
    app.dependency_overrides = {}

# CREATE BOOK TESTS
@pytest.mark.asyncio
async def test_create_book_success(async_client, mock_db):
    # Setup mock
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    response = await async_client.post("/", json=test_book)
    
    assert response.status_code == 200
    assert response.json()["title"] == test_book["title"]
    assert response.json()["author"] == test_book["author"]
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

# GET BOOKS TESTS
@pytest.mark.asyncio
async def test_get_books_success(async_client, mock_db):
    # Setup mock books
    mock_books = [
        Book(id=1, **test_book),
        Book(id=2, title="Book 2", author="Author 2", summary="Summary 2")
    ]
    mock_result = AsyncMock()
    mock_result.scalars.return_value.all.return_value = mock_books
    mock_db.execute.return_value = mock_result

    response = await async_client.get("/")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    mock_db.execute.assert_called_once()

# GET SINGLE BOOK TESTS
@pytest.mark.asyncio
async def test_get_book_success(async_client, mock_db):
    # Setup mock book
    mock_book = Book(id=1, **test_book)
    mock_result = AsyncMock()
    mock_result.scalars.return_value.first.return_value = mock_book
    mock_db.execute.return_value = mock_result

    response = await async_client.get("/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == test_book["title"]

@pytest.mark.asyncio
async def test_get_book_not_found(async_client, mock_db):
    # Setup mock to return None
    mock_result = AsyncMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    response = await async_client.get("/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

# UPDATE BOOK TESTS
@pytest.mark.asyncio
async def test_update_book_success(async_client, mock_db):
    # Setup mock book
    mock_book = Book(id=1, **test_book)
    mock_result = AsyncMock()
    mock_result.scalars.return_value.first.return_value = mock_book
    mock_db.execute.return_value = mock_result
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()

    updated_data = {
        "title": "Updated Title",
        "author": "Updated Author",
        "summary": "Updated Summary"
    }

    response = await async_client.put("/1", json=updated_data)
    
    assert response.status_code == 200
    assert response.json()["title"] == updated_data["title"]
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_update_book_not_found(async_client, mock_db):
    mock_result = AsyncMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    response = await async_client.put("/999", json=test_book)
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

# DELETE BOOK TESTS
@pytest.mark.asyncio
async def test_delete_book_success(async_client, mock_db):
    # Setup mock book
    mock_book = Book(id=1, **test_book)
    mock_result = AsyncMock()
    mock_result.scalars.return_value.first.return_value = mock_book
    mock_db.execute.return_value = mock_result
    mock_db.commit = AsyncMock()

    response = await async_client.delete("/1")
    
    assert response.status_code == 200
    assert response.json()["id"] == 1
    mock_db.delete.assert_called_once_with(mock_book)
    mock_db.commit.assert_called_once()

@pytest.mark.asyncio
async def test_delete_book_not_found(async_client, mock_db):
    mock_result = AsyncMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    response = await async_client.delete("/999")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

# BOOK SUMMARY TESTS
@pytest.mark.asyncio
async def test_get_book_summary_with_reviews(async_client, mock_db):
    # Setup mock book
    mock_book = Book(id=1, **test_book)
    mock_book_result = AsyncMock()
    mock_book_result.scalars.return_value.first.return_value = mock_book
    
    # Setup mock reviews
    mock_reviews = [
        Review(id=1, book_id=1, rating=4),
        Review(id=2, book_id=1, rating=5)
    ]
    mock_reviews_result = AsyncMock()
    mock_reviews_result.scalars.return_value.all.return_value = mock_reviews
    
    # Configure mock_db to return different results for different queries
    mock_db.execute.side_effect = [mock_book_result, mock_reviews_result]

    response = await async_client.get("/1/summary")
    
    assert response.status_code == 200
    assert response.json()["book_id"] == 1
    assert response.json()["average_rating"] == 4.5  # (4 + 5) / 2

@pytest.mark.asyncio
async def test_get_book_summary_no_reviews(async_client, mock_db):
    # Setup mock book
    mock_book = Book(id=1, **test_book)
    mock_book_result = AsyncMock()
    mock_book_result.scalars.return_value.first.return_value = mock_book
    
    # Setup empty reviews
    mock_reviews_result = AsyncMock()
    mock_reviews_result.scalars.return_value.all.return_value = []
    
    # Configure mock_db to return different results for different queries
    mock_db.execute.side_effect = [mock_book_result, mock_reviews_result]

    response = await async_client.get("/1/summary")
    
    assert response.status_code == 200
    assert response.json()["book_id"] == 1
    assert response.json()["average_rating"] == 0

@pytest.mark.asyncio
async def test_get_book_summary_not_found(async_client, mock_db):
    mock_result = AsyncMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db.execute.return_value = mock_result

    response = await async_client.get("/999/summary")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"
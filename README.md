# Intelligent_Book_Management_System
This repository holds the code for coding assessment for Senior Consultant- Gen AI- an intelligent book management system using Llama 3.2(Ollama), Fast API, PostgreSQL, and Embedding model to generate recommendation based on user search.

This project implements an intelligent book management system that integrates with FastAPI, PostgreSQL, and Ollama's Llama3 model. It supports authentication, CRUD operations for books and reviews, and user-based book recommendations. The system also utilizes JWT authentication for securing API routes.

## 1. System Requirements
* Python 3.8+: The system is built using Python 3.8 or higher.
* PostgreSQL: PostgreSQL is used as the database for storing book and user information.
* Ollama: Llama3 generative AI model is used for book summary generation.
* FastAPI: FastAPI is used for creating the RESTful API.
* Uvicorn: Uvicorn is the ASGI server to run FastAPI in production.
* Sentence Transformer: Embedding model to generate recommendations based on matching of embeddings using cosine similarity.


## 2. Project Dependencies

### 2.1 Project Dependencies

* FastAPI: For building the web API.
* Uvicorn: ASGI server for FastAPI applications.
* SQLAlchemy: ORM to interact with PostgreSQL asynchronously.
* asyncpg: PostgreSQL async driver for SQLAlchemy.
* Pydantic: For data validation and serialization of API request/response models.
* JOS (JSON Web Token): For generating and validating JWT tokens.
* Passlib: For password hashing and verification.
* python-dotenv: For loading environment variables from .env file.
* pytest: For running unit tests.
* httpx: For making HTTP requests during tests.
* Ollama (Client): For interacting with the Llama3 AI model.

### 2.2 Installation

1. Clone the repository

```bash
git clone <repository_url>
```
2. Create and activate a Python virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```
3. Install the dependencies:

```bash
pip install -r requirements.txt
```
4. Install Ollama model locally

```
Download ollama from https://ollama.com/download
Install ollama and add it to system PATH
Open terminal and :
ollama pull llama3.2
```

### 2.3 Environment Variables

Create a .env file in root folder and add these:

1. DATABASE_URL: The URL for your PostgreSQL database connection. Example:
```
DATABASE_URL=postgresql+asyncpg://username:password@localhost/bookdb
```
2. JWT_SECRET_KEY: A secret key for encoding and decoding JWT tokens. Example:
```
SECRET_KEY=your_jwt_secret_key
```
3. JWT_ALGORITHM: The algorithm used to encode and decode JWT tokens. Example:
```
ALGORITHM=HS256
```
4. JWT_EXPIRATION_TIME_MINUTES: The expiration time of JWT tokens in minutes. Example:
```
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
5. OLLAMA_MODEL: Ollama Model with version to use:
```
OLLAMA_MODEL='llama3.2'
```
6. CHUNK_SIZE: Chunk size of documents to divide into smaller chunks for parallel processing and summary generation.
```
CHUNK_SIZE=2000
```
7. MAX_WORKERS: Number of simultaneous processes that will run in parallel for chunk summary generation.
```
MAX_WORKERS=10
```
8. EMBEDDING_MODEL: Model to use embedding of books data and user query for generating recommendation.
```
EMBEDDING_MODEL="all-MiniLM-L6-v2"
```

## 3. Database Setup

PostgreSQL has been used to create Database and subsequent tables - books, reviews and users. The application uses SQLAlchemy for interacting with PostgreSQL. The tables are created on application startup.

## 4. Start the Application

Run the FastAPI application using Uvicorn:
```
uvicorn app.main:app --reload
```
* The --reload option automatically reloads the server when you make changes to the code.
* The application will be available at http://127.0.0.1:8000

## 5. Access the API Documentation

You can view the interactive API documentation generated by FastAPI by going to:

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc UI: http://127.0.0.1:8000/redoc
  
These interfaces let you explore and test the API endpoints directly from your browser.

## 6. esting the Application
To run the tests:

Ensure testing dependencies are installed (already included in requirements.txt).

Run tests using pytest:

```bash
pytest
```
Test results and coverage will be displayed in the console.

## 7. Using Authentication
Register a new user by sending a POST request to /auth/sign-up.

Login with the created user credentials at /auth/login to receive a JWT token.

Use this JWT token for authorization on protected endpoints by adding it to the Authorization header as a Bearer token:
```
Authorization: Bearer <jwt_token>
```

## 8. Application Endpoints
8.1 Book Management Endpoints
POST /api/books: Add a new book.
Request Body: { "title": "Book Title", "author": "Author Name", "genre": "Fiction", "year_published": 2021 }
Response: The created book object.

GET /api/books: Retrieve all books.
Response: List of all books.

GET /api/books/{id}: Retrieve a book by ID.
Path Param: id (integer)
Response: Book object.

PUT /api/books/{id}: Update a book's information by ID.
Path Param: id (integer)
Request Body: { "title": "New Title", "author": "New Author", "genre": "New Genre", "year_published": 2022 }
Response: Updated book object.

DELETE /api/books/{id}: Delete a book by ID.
Path Param: id (integer)
Response: Success message.

POST /summaries/generate-summary: Generate a summary for a book by ID.
Request Body: {"content": "content of book to be summarized"}
Response: Generated summary for the book.

8.2 Review Management Endpoints

POST /reviews/{id}: Add a review for a book.
Path Param: id (integer)
Request Body: { "user_id": 1, "review_text": "Great book!", "rating": 5 }
Response: Created review object.

GET /reviews/{id}: Retrieve all reviews for a book.
Path Param: id (integer)
Response: List of reviews for the book.

8.3 User Authentication Endpoints

POST /auth/sign-up: Register a new user.
Request Body: { "username": "user1", "email":"email", "password": "password" }
Response: Created user object.

POST /auth/login: Login and receive a JWT token.
Request Body: { "username": "user1", "password": "password" }
Response: { "access_token": "jwt_token", "token_type": "bearer" }

8.4 Book Recommendations Endpoint

GET /api/recommendations: Get book recommendations based on user preferences (future feature).
Request Body: { "content":"user query" }
Response: list of matching titles of books

## Key Features Implemented

* Modular approach to all the routes making the code easy to maintain.
* Singleton implementation of Database and Llama3 classes to ensure only one instance gets spun up for one requesting entity.
* Chunking of book content and parallel processing of all chunks included to handle the limited context window of Large Language Models.
* Embedding models are used to create embeddings of Book records in books table. These embeddings are then matched with user query's embedding to return a highly matching book (top 2).

## Future imrovements

* Implementation of vector database (like Pinecone) to store book data embeddings and then use cosine similarity to match user query embedding. This proves to be way faster than normal search.
* Cloud implementation to handle multiple requests and application scalability.






   

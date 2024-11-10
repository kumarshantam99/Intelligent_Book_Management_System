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

```bash git clone <repository_url> ``` 

2. Create and activate a Python virtual environment:

```bash python3 -m venv venv source venv/bin/activate  # On Windows, use venv\Scripts\activate ```

"""Module to handle constants used"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


# Load environment variables from .env file
load_dotenv()
class Settings(BaseSettings):
    """Reading .env files"""
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    OLLAMA_MODEL: str = os.getenv('OLLAMA_MODEL')
    CHUNK_SIZE: int = os.getenv('CHUNK_SIZE')
    MAX_WORKERS: int = os.getenv('MAX_WORKERS')
    EMBEDDING_MODEL: str = os.getenv('EMBEDDING_MODEL')

settings = Settings()

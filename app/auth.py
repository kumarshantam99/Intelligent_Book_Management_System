"""Module to handle authentication and get current user id after authentication"""
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.hash import argon2
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def create_access_token(data: dict):
    """Create Access Token"""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password using argon2."""
    return argon2.verify(plain_password, hashed_password)

async def get_password_hash(password: str) -> str:
    """Hash password using argon2."""
    return argon2.hash(password)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    """Get Current user ID using received JWT Token"""
    print("Token received in get_current_user:", token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print("Decoded Payload:", payload)  # Add this for debugging       
        
        user_id_str = payload.get("sub")
        
        if user_id_str is None:
            raise credentials_exception
        
        # Convert user_id to an integer before querying
        user_id = int(user_id_str)

        return user_id  # Return the full user object instead of username
    except JWTError:
        raise credentials_exception

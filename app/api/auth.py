"""Module to handle auth routes"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas, utils
from app.database import get_db
from app.auth import get_password_hash

router = APIRouter()

# Sign-up endpoint
@router.post("/sign-up", response_model=schemas.UserResponse)
async def sign_up(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """Check if the username already exists"""
    result = await db.execute(select(models.User).filter(models.User.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if the email already exists
    result_email = await db.execute(select(models.User).filter(models.User.email == user.email))
    existing_email = result_email.scalars().first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = await get_password_hash(user.password)
    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # Return the user response model without the password
    return schemas.UserResponse(username=new_user.username, email=new_user.email)
 
@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    """Login endpoint"""
    # Use async query with `select()`
    result = await db.execute(select(models.User).filter(models.User.username == user.username))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not utils.verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    access_token = utils.create_access_token(data={"sub": str(existing_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreateSchema
from app.services import users_service

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    user = users_service.create_user(db, user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return {"message": "User registered successfully", "username": user_data.nome}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserAuth
from app.services import auth_service

router = APIRouter()

@router.post("/login")
async def login(user_auth: UserAuth, db: Session = Depends(get_db)):
    authenticated = auth_service.check_authentication(db, user_auth.nome, user_auth.pswd)
    if not authenticated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    return {"message": f"User {user_auth.nome} authenticated successfully"}

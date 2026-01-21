from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserAuth
from app.services import auth_service
from app.core.security import create_access_token
from app.schemas.token_response_schema import TokenResponseSchema

router = APIRouter()

@router.post("/login", response_model=TokenResponseSchema)
async def login(user_auth: UserAuth, db: Session = Depends(get_db)):
    user = auth_service.check_authentication(db, user_auth.nome, user_auth.pswd)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from src.app.api.dependencies import get_db
from src.app.schemas.user import LoginSchema, TokenSchema, UserCreate
from src.app.services.auth_service import AuthService
from src.app.core.logging import logger
router = APIRouter()

@router.post("/register", response_model=TokenSchema)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info("Register route called", user.email)
        db_user = AuthService.register(user, db)
        
        access_token = AuthService.create_access_token({"sub": str(db_user.id)})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenSchema)
def login(user: LoginSchema, db: Session = Depends(get_db)):
    logger.info("Login route called", user.email)

    access_token = AuthService.login(user, db)
    if not access_token:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    return {"access_token": access_token, "token_type": "bearer"}

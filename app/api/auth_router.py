from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schema.auth_schema import LoginRequest, Token
from app.services import auth_service

from app.core.database import get_db
from app.schema.user_schema import UserCreate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, payload)
    return user


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    access_token, refresh_token = auth_service.login_user(
        db, payload.email, payload.password
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
def refresh(token: str, db: Session = Depends(get_db)):
    new_access_token = auth_service.refresh_access_token(db, token)
    return {
        "access_token": new_access_token,
        "refresh_token": token,
        "token_type": "bearer",
    }


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(token: str, db: Session = Depends(get_db)):
    auth_service.logout_user(db, token)

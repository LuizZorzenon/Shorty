from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repository import user_repository, refresh_token_repository
from app.core.security import verify_password, create_access_token, create_refresh_token


def login_user(db: Session, email: str, password: str):
    user = user_repository.get_by_email(db, email)

    if not user or not verify_password(password, str(user.hashed_password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token, expires_at = create_refresh_token()

    refresh_token_repository.create(
        db=db,
        token=refresh_token,
        user_id=user.id,
        expires_at=expires_at,
    )

    return access_token, refresh_token


def refresh_access_token(db: Session, token: str):
    db_token = refresh_token_repository.get_by_token(db, token)

    if not db_token or db_token.is_revoked or db_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    new_access_token = create_access_token({"sub": str(db_token.user_id)})
    return new_access_token


def logout_user(db: Session, token: str):
    db_token = refresh_token_repository.get_by_token(db, token)

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Token not found"
        )

    refresh_token_repository.revoke(db=db, token=token)

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.refresh_token import RefreshToken


def create(db: Session, token: str, user_id: int, expires_at: datetime) -> RefreshToken:
    refresh_token = RefreshToken(
        token=token,
        user_id=user_id,
        expires_at=expires_at,
        is_revoked=False,
    )
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return refresh_token


def get_by_token(db: Session, token: str) -> RefreshToken | None:
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()


def revoke(db: Session, token: str) -> None:
    db.query(RefreshToken).filter(RefreshToken.token == token).update(
        {"is_revoked": True}
    )
    db.commit()

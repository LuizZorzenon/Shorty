from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timezone, UTC

from app.core.settings import settings
from app.core.database import get_db
from app.repository import user_repository

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": False},
        )

        exp = payload.get("exp")

        if exp is None:
            raise HTTPException(status_code=401, detail="Token missing expiration")

        expires_at = datetime.fromtimestamp(exp, tz=UTC)

        if expires_at < datetime.now(UTC):
            raise HTTPException(status_code=401, detail="Token expired")

        user_id: str = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = user_repository.get_by_id(db, int(user_id))

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

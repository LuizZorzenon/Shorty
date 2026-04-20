from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repository import user_repository
from app.schema.user_schema import UserCreate
from app.core.security import hash_password


def create_user(db: Session, payload: UserCreate):
    existing_email = user_repository.get_by_email(db, payload.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    existing_username = user_repository.get_by_username(db, payload.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )

    hashed_password = hash_password(payload.password)

    user = user_repository.create(
        db=db,
        email=payload.email,
        username=payload.username,
        hashed_password=hashed_password,
    )

    return user

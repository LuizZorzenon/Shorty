from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
import string
import random

from app.core.database import get_db
from typing import List
from app.core.deps import get_current_user
from app.models.user import User
from app.services import url_service
from app.schema.url_schema import URLRequest, URLResponse

router = APIRouter(prefix="/urls", tags=["URLs"])


@router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create_url(
    payload: URLRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    url = url_service.create_short_url(
        db=db, original_url=payload.original_url, user_id=current_user.id  # type: ignore
    )

    return url


@router.get("/", response_model=List[URLResponse], status_code=status.HTTP_200_OK)
def list_urls(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return url_service.get_all_urls(db=db, user_id=current_user.id)


@router.get("/{shortkey}", response_model=URLResponse, status_code=status.HTTP_200_OK)
def get_url_by_shortkey(
    shortkey: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    url = url_service.get_by_shortkey(db=db, shortkey=shortkey, user_id=current_user.id)

    return url


@router.patch("/{shortkey}", response_model=URLResponse, status_code=status.HTTP_200_OK)
def update_url_by_shortkey(
    shortkey: str,
    data: URLRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    url = url_service.get_by_shortkey(db=db, shortkey=shortkey, user_id=current_user.id)

    new_url = data

    url_updated = url_service.update_url_by_shortkey(
        db=db, shortkey=url.short_key, data=new_url
    )

    return url_updated


@router.delete("/{shortkey}", status_code=status.HTTP_200_OK)
def delete_url_by_shortkey(
    shortkey: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    url_service.delete_url_by_shortkey(db=db, shortkey=shortkey, user_id=current_user)

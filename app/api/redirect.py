from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repository import url_repository

router = APIRouter(tags=["Redirect"])


@router.get("/{short_key}")
def redirect(short_key: str, db: Session = Depends(get_db)):
    url = url_repository.get_by_shortkey(db, short_key)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    if not url.is_active:
        raise HTTPException(status_code=410, detail="URL disabled")

    url.clicks += 1
    db.commit()

    return RedirectResponse(url.original_url)  # type: ignore

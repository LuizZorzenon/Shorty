from sqlalchemy.orm import Session

from app.models.url import URL

allowed_fields = {"original_url", "is_active"}


def get_by_shortkey(db: Session, shortkey: str) -> URL | None:
    return db.query(URL).filter(URL.short_key == shortkey).first()


def get_by_user(db: Session, user_id: int) -> list[URL]:
    return db.query(URL).filter(URL.owner_id == user_id).all()


def delete_by_shortkey(db: Session, shortkey: str) -> str:
    db.query(URL).filter(URL.short_key == shortkey).delete()
    db.commit()

    return "URL deletada com sucesso!"


def update_url_by_shortkey(db: Session, shortkey: str, data: dict) -> URL | None:
    url = db.query(URL).filter(URL.short_key == shortkey).first()

    if not url:
        return None  # pragma: no cover

    for key, value in data.items():
        if key in allowed_fields:
            setattr(url, key, value)

    db.commit()
    db.refresh(url)

    return url


def create(
    db: Session,
    original_url: str,
    short_key: str,
    owner_id: int,
    is_active: bool = True,
) -> URL:
    url = URL(
        original_url=original_url,
        short_key=short_key,
        owner_id=owner_id,
        is_active=is_active,
    )

    db.add(url)
    db.commit()
    db.refresh(url)

    return url

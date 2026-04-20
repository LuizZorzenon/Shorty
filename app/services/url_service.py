from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repository import url_repository
from app.utils.generate_shortkey import generate_short_key


def create_short_url(db: Session, original_url: str, user_id: int):
    short_key = generate_short_key()

    return url_repository.create(
        db=db,
        original_url=original_url,
        short_key=short_key,
        owner_id=user_id,
    )


def get_by_shortkey(db: Session, shortkey: str, user_id: int):

    url = url_repository.get_by_shortkey(db=db, shortkey=shortkey)

    if not url:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="URL not found"
        )

    if url.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not have access to this Url or url does not exists",
        )

    return url


def get_all_urls(db: Session, user_id: int):

    url = url_repository.get_by_user(db=db, user_id=user_id)

    if url == []:
        pass
    elif not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This user not have urls"
        )

    return url


def update_url_by_shortkey(db: Session, shortkey: str, data: dict):

    url = url_repository.get_by_shortkey(db=db, shortkey=shortkey)

    if not url:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="URL not found"
        )

    new_url = url_repository.update_url_by_shortkey(
        db=db, shortkey=shortkey, data=data.model_dump(exclude_unset=True)
    )

    return new_url


def delete_url_by_shortkey(db: Session, shortkey: str) -> str:

    url = url_repository.get_by_shortkey(db=db, shortkey=shortkey)

    if not url:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="URL not found"
        )

    url_repository.delete_by_shortkey(db=db, shortkey=shortkey)

    return "URL deletada com sucesso!"

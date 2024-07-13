from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..models.code import Code
from ..utils.generate_codes import generate_short_code
from ..schemas.shorten_schemas import UrlShortenSchema, CreateShortenUrlUserSchema


def create_short_url(original_url: str, db: Session) -> UrlShortenSchema:
    code = generate_short_code()
    new_short_url = Code(original_url=original_url, code=code)
    db.add(new_short_url)
    db.commit()
    db.refresh(new_short_url)
    shorten_url = UrlShortenSchema(shorten_url=f"http://localhost/{new_short_url.code}")
    return shorten_url


def create_short_url_by_user(
    data: CreateShortenUrlUserSchema, user: str, db: Session
) -> UrlShortenSchema:
    user_db = db.query(User).filter(User.user_name == user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    code = generate_short_code()
    new_short_url_user = Code(
        original_url=data.original_url,
        title=data.title,
        code=code,
        user=user_db,
    )
    db.add(new_short_url_user)
    db.commit()
    db.refresh(new_short_url_user)
    shorten_url = UrlShortenSchema(
        shorten_url=f"http://localhost/{new_short_url_user.code}"
    )
    return shorten_url

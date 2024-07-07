from sqlalchemy.orm import Session
from ..database import models
from ..utils.generate_codes import generate_short_code
from .shorten_schemas import UrlShortenSchema


def create_short_url(original_url: str, db: Session) -> UrlShortenSchema:
    code = generate_short_code()
    new_short_url = models.Code(original_url=original_url, code=code)
    db.add(new_short_url)
    db.commit()
    db.refresh(new_short_url)
    shorten_url = UrlShortenSchema(shorten_url=f"http://localhost/{new_short_url.code}")
    return shorten_url

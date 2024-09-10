from sqlmodel import Session, select
from fastapi import HTTPException, status
from ..models.user import User
from ..models.code import Code, ShortUrlCreate, ShortUrlSResponse
from ..utils.generate_codes import generate_short_code
import dotenv
import os

dotenv.load_dotenv()

DOMAIN_NAME = os.environ.get("DOMAIN_URL")


def create_short_url(original_url: str, session: Session) -> ShortUrlSResponse:
    code = generate_short_code()
    try:
        new_short_url = Code(original_url=original_url, code=code)
        session.add(new_short_url)
        session.commit()
        session.refresh(new_short_url)
        shorten_url = ShortUrlSResponse(
            id=new_short_url.id,
            shorten_url=f"{DOMAIN_NAME}{new_short_url.code}",
            original_url=new_short_url.original_url,
        )
        return shorten_url
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error."},
        )


def create_short_url_by_user(
    data: ShortUrlCreate, user: str, session: Session
) -> ShortUrlSResponse:
    try:
        statement = select(User).where(User.username == user)
        user_db = session.exec(statement).first()
        if not user_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
            )
        code = generate_short_code()
        new_short_url_user = Code(
            original_url=str(data.original_url),
            title=data.title,
            code=code,
            user=user_db,
        )
        session.add(new_short_url_user)
        session.commit()
        session.refresh(new_short_url_user)
        shorten_url = ShortUrlSResponse(
            id=new_short_url_user.id,
            shorten_url=f"{DOMAIN_NAME}{new_short_url_user.code}",
            original_url=new_short_url_user.original_url,
            title=new_short_url_user.title,
        )
        return shorten_url
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error"},
        )

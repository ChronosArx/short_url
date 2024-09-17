import qrcode.constants
from sqlmodel import Session, select
from fastapi import HTTPException, status
from ..models.user import User
from ..models.code import Code, ShortUrlCreate, ShortUrlSResponse
from ..utils.generate_codes import generate_short_code
from ..core.config import settings
import qrcode
import io


def create_short_url(original_url: str, session: Session) -> ShortUrlSResponse:
    code = generate_short_code()
    try:
        new_short_url = Code(original_url=original_url, code=code)
        session.add(new_short_url)
        session.commit()
        session.refresh(new_short_url)
        shorten_url = ShortUrlSResponse(
            id=new_short_url.id,
            shorten_url=f"{settings.get_domain_name()}{new_short_url.code}",
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
            shorten_url=f"{settings.get_domain_name()}{new_short_url_user.code}",
            original_url=new_short_url_user.original_url,
            title=new_short_url_user.title,
        )
        return shorten_url
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error"},
        )


def generate_qr(url:str) :
    qr = qrcode.QRCode(
        version=1,
        box_size = 10,
        border=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
    )

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    
    # seek(0) indica colocar el buffer al inicio
    img_byte_arr.seek(0)

    return img_byte_arr
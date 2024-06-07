from fastapi import APIRouter
from ..utils.generate_codes import generate_short_code
from starlette.responses import RedirectResponse

router = APIRouter()

test_urls = {}


@router.get("/short_url_free")
async def get_free_short_url(original_url: str):
    code = generate_short_code()
    test_urls[code] = original_url
    return {"originalUrl": original_url, "shortCode": code}


@router.get("/{code}")
async def redirect_original(code:str):
    return RedirectResponse(url=test_urls[code])

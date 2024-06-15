from fastapi import APIRouter

router = APIRouter()


@router.get("/premium", tags=["Premium"])
async def get_premium_link():
    return {"Message": "Hello this is premium"}

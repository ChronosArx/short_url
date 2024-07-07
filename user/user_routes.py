from fastapi import APIRouter

router = APIRouter(prefix="/user")


@router.get("/codes")
async def get_all_codes():
    pass


@router.get("/code/{code_id}")
async def get_code():
    pass


@router.delete("/code/{code_id}")
async def delate_code():
    pass

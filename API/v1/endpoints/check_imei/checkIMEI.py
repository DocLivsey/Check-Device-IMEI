from fastapi import APIRouter

from v1.schemas.checkIMEI import HelloScheme

check_imei_router = APIRouter()


@check_imei_router.get('/hello/', response_model=HelloScheme)
async def hello():
    pass

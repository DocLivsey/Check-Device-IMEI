from fastapi import APIRouter, Request
import structlog
import requests

logger = structlog.get_logger(__name__)

from v1.schemas.checkIMEI import HelloScheme

check_imei_router = APIRouter()


@check_imei_router.get('/hello/', response_model=HelloScheme)
async def hello(request: Request):
    pass

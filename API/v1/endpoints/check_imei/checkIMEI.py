from fastapi import APIRouter, Request, HTTPException
import structlog
import requests

logger = structlog.get_logger(__name__)

from v1.schemas.checkIMEI import HelloScheme, to_message
from settings import server_host, api_base_path, api_version

check_imei_router = APIRouter()


@check_imei_router.get('/', response_model=HelloScheme)
async def check_imei(request: Request):
    pass

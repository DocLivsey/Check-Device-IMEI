from fastapi import APIRouter, Request, HTTPException, status
import structlog
import requests

logger = structlog.get_logger(__name__)

from v1.schemas.checkIMEI import HelloScheme, to_message
from settings import server_host, api_base_path, api_version

check_imei_router = APIRouter()


@check_imei_router.get('/', response_model=HelloScheme)
async def check_imei(request: Request):
    logger.info(
        'Handle GET request to API for check device IMEI',
        request=request,
    )
    
    request_headers = request.headers
    
    if 'authorization' not in request_headers.keys():
        logger.error(
            'Authorization header missing',
            request_headers=request.headers,
            request_body=await request.body(),
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization header missing')

    if not request_headers['Authorization'].startswith('Token '):
        logger.error(
            'Authorization header invalid',
            request_headers=request.headers,
            request_body=await request.body(),
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization header invalid')

    if not request_headers['Authorization']:
        logger.error(
            'Authorization token missing',
            request_headers=request.headers,
            request_body=await request.body(),
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization token missing')
    
    url = f'{server_host}{api_base_path}{api_version}/check-imei/'
    imei_check_url = 'https://api.imeicheck.net/v1/checks'
    headers: dict = {
        'Authorization': request_headers['authorization']
    }
    response: requests.Response

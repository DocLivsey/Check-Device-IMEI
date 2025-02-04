from fastapi import APIRouter, Request, HTTPException, status
import structlog
import requests

from v1.functiontools import handle_401_response

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
    
    handle_401_response(request_headers)
    
    url = f'{server_host}{api_base_path}{api_version}/check-imei/'
    imei_check_url = 'https://api.imeicheck.net/v1/checks'
    headers: dict = {
        'Authorization': request_headers['authorization']
    }
    response: requests.Response
    try:
        logger.debug(
            'Get data from bot`s request and trying to Send POST request to get info about device',
            endpoint=imei_check_url,
            headers=headers,
        )

    except Exception as e:
        pass

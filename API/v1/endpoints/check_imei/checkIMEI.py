import requests
import structlog
from fastapi import APIRouter, Request, HTTPException, status

from v1.functiontools import handle_401_response

logger = structlog.get_logger(__name__)

from v1.schemas.checkIMEI import IMEICheckScheme
from settings import server_host, api_base_path, api_version, imei_check_api_token

check_imei_router = APIRouter()

DEFAULT_SERVICE_ID = 1


@check_imei_router.get('/', response_model=IMEICheckScheme)
async def check_imei(request: Request):
    logger.info(
        'Handle GET request to API for check device IMEI',
        request_headers=request.headers,
        request_body=await request.json(),
    )
    
    request_headers = request.headers
    request_body = await request.json()
    
    handle_401_response(request_headers)
    
    url = f'{server_host}{api_base_path}{api_version}/check-imei/'
    imei_check_url = 'https://api.imeicheck.net/v1/checks'
    headers: dict = {
        'Authorization': f'Bearer {imei_check_api_token}'
    }
    response: requests.Response
    imei: str = request_body.get('imei')
    body = {
        'deviceId': imei,
        'serviceId': DEFAULT_SERVICE_ID,
    }
    try:
        logger.debug(
            'Get data from bot`s request and trying to Send POST request to get info about device',
            endpoint=imei_check_url,
            headers=headers,
            body=request_body,
            imei=imei,
        )

        response = requests.post(
            url=imei_check_url,
            headers=headers,
            json=body,
        )
    except HTTPException as http_exception:
        logger.error(
            'HTTP error occurred',
            http_error=str(http_exception),
            endpoint=imei_check_url,
            body=body,
        )

        raise HTTPException(
            status_code=http_exception.status_code,
            detail=http_exception.detail,
        )

    except Exception as exception:
        logger.error(
            'Exception occurred',
            exc_info=exception,
            endpoint=url,
            body=body,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
        )

    if response.status_code != status.HTTP_200_OK:
        logger.error(
            'Failed to get data about device by IMEI',
            status_code=response.status_code,
            reason=response.reason,
            response=response.text,
            imei=imei,
        )

        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )

    return IMEICheckScheme.to_response(response.json())

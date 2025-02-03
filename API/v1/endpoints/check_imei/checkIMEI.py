from fastapi import APIRouter, Request, HTTPException
import structlog
import requests

logger = structlog.get_logger(__name__)

from v1.schemas.checkIMEI import HelloScheme, to_message
from settings import server_host, api_base_path, api_version

check_imei_router = APIRouter()


@check_imei_router.get('/hello/', response_model=HelloScheme)
async def hello(request: Request):
    logger.info(
        'Handle POST request to API for Telegram token authentication with',
        request_headers=request.headers,
        request_body=request.json(),
    )

    if 'Authorization' or 'authorization' not in request.headers.keys():
        raise HTTPException(status_code=401, detail='Authorization header missing')

    if not request.headers['Authorization'].startswith('Token '):
        raise HTTPException(status_code=401, detail='Authorization header invalid')

    if not request.headers['Authorization']:
        raise HTTPException(status_code=401, detail='Authorization token missing')

    url = f'{server_host}{api_base_path}{api_version}/hello/'
    response: requests.Response
    try:
        logger.info(
            'Trying to send request to Django server REST API endpoint',
            headers=request.headers,
            endpoint=url,
        )

        response = requests.get(
            url=url,
            headers=request.headers,
        )
    except HTTPException as http_exception:
        logger.error(
            'HTTP error occurred',
            http_error=str(http_exception),
            endpoint=url,
            headers=request.headers,
        )

        raise HTTPException(status_code=http_exception.status_code, detail=str(http_exception))
    except Exception as exception:
        logger.error(
            'Exception occurred',
            exc_info=exception,
            endpoint=url,
            headers=request.headers,
        )

        raise HTTPException(status_code=400, detail=str(exception))

    logger.info(
        'Successfully retrieved message from Django server REST API',
        message=response.json().get('message'),
        endpoint=url,
    )

    return to_message(response.json())

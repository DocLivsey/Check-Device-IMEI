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
        'Handle POST request to API to send Welcome message to user',
        request_headers=request.headers,
        request_body=await request.body(),
    )

    if 'authorization' not in request.headers.keys():
        logger.error(
            'Authorization header missing',
            request_headers=request.headers,
            request_body=await request.body(),
        )
        
        raise HTTPException(status_code=401, detail='Authorization header missing')

    if not request.headers['Authorization'].startswith('Token '):
        logger.error(
            'Authorization header invalid',
            request_headers=request.headers,
            request_body=await request.body(),
        )
        
        raise HTTPException(status_code=401, detail='Authorization header invalid')

    if not request.headers['Authorization']:
        logger.error(
            'Authorization token missing',
            request_headers=request.headers,
            request_body=await request.body(),
        )
        
        raise HTTPException(status_code=401, detail='Authorization token missing')

    url = f'{server_host}{api_base_path}{api_version}/hello/'
    response: requests.Response
    try:
        logger.info(
            'Trying to send request to Django server REST API endpoint',
            headers=request.headers,
            body=await request.body(),
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
            body=await request.body(),
            headers=request.headers,
        )

        raise HTTPException(status_code=http_exception.status_code, detail=str(http_exception))
    
    except Exception as exception:
        logger.error(
            'Exception occurred',
            exc_info=exception,
            endpoint=url,
            body=await request.body(),
            headers=request.headers,
        )

        raise HTTPException(status_code=400, detail=str(exception))

    logger.info(
        'Successfully retrieved message from Django server REST API',
        message=response.json().get('message'),
        endpoint=url,
    )

    return to_message(response.json())

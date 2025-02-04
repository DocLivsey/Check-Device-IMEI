from fastapi import APIRouter, Request, HTTPException, status
import structlog
import requests

from v1.functiontools import handle_401

logger = structlog.get_logger(__name__)

from v1.routers.auth import router as auth_router
from v1.routers.checkIMEI import router as check_imei_router
from v1.schemas.checkIMEI import HelloScheme, to_message
from settings import server_host, api_base_path, api_version

router = APIRouter()

router.include_router(auth_router)
router.include_router(check_imei_router)


@router.get('/hello/', response_model=HelloScheme)
async def hello(request: Request):
    logger.info(
        'Handle POST request to API to send Welcome message to user',
        request_headers=request.headers,
        request_body=await request.body(),
    )

    handle_401(request.headers)

    url = f'{server_host}{api_base_path}{api_version}/hello/'
    headers: dict = {
        'Authorization': request.headers['authorization']
    }
    response: requests.Response
    try:
        logger.info(
            'Trying to send request to Django server REST API endpoint',
            headers=headers,
            body=await request.body(),
            endpoint=url,
        )

        response = requests.get(
            url=url,
            headers=headers,
        )
    except HTTPException as http_exception:
        logger.error(
            'HTTP error occurred',
            http_error=str(http_exception),
            endpoint=url,
            headers=headers,
        )

        raise HTTPException(status_code=http_exception.status_code, detail=str(http_exception))

    except Exception as exception:
        logger.error(
            'Exception occurred',
            exc_info=exception,
            endpoint=url,
            headers=headers,
        )

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))

    if response.status_code == 401:
        logger.error(
            'Authorization failed',
            status_code=response.status_code,
            request_headers=headers,
            endpoint=url,
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization failed')

    if response.status_code == 403:
        logger.error(
            'User was blocked',
            status_code=response.status_code,
            request_headers=headers,
            endpoint=url,
        )

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User was blocked')

    logger.info(
        'Successfully retrieved message from Django server REST API',
        message=response.json().get('message'),
        endpoint=url,
    )

    return to_message(response.json().get('message'))


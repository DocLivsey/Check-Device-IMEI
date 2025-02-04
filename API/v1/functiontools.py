from fastapi import status, HTTPException
from fastapi.datastructures import Headers
import structlog

logger = structlog.get_logger(__name__)


def handle_401_response(headers: Headers):
    if 'authorization' not in headers.keys():
        logger.error(
            'Authorization header missing',
            request_headers=headers,
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization header missing')

    if not headers['Authorization'].startswith('Token '):
        logger.error(
            'Authorization header invalid',
            request_headers=headers,
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization header invalid')

    if not headers['Authorization']:
        logger.error(
            'Authorization token missing',
            request_headers=headers,
        )

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authorization token missing')
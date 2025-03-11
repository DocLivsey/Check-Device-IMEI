from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from pydantic import ValidationError
import structlog
import requests

logger = structlog.get_logger(__name__)

from settings import api_url_take_token, server_host, api_base_path, api_version
from v1.schemas.auth import TokenSchema, TelegramUserSchema, to_telegram_user, to_token

auth_router = APIRouter()


@auth_router.post(f'{api_url_take_token}', response_model=TokenSchema)
async def telegram_token_auth(from_user_data: TelegramUserSchema):
    logger.info(
        'Handle POST request to API for Telegram token authentication with',
        data_from_user=from_user_data,
    )
    
    url = f'{server_host}{api_base_path}{api_version}{api_url_take_token}'
    response: requests.Response
    try:
        logger.debug(
            'Successfully mapping user data to TelegramUserSchema and '
            'trying to send request to Django server REST API endpoint',
            telegram_user=from_user_data.dict(),
            endpoint=url
        )

        response = requests.post(
            url=url,
            json=from_user_data.dict(),
        )
    except ValidationError as validation_error:
        logger.error(
            'Validation error occurred',
            validation_error=validation_error.json(),
            endpoint=url,
            data_from_user=from_user_data,
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=validation_error.json()
        )

    except HTTPException as http_exception:
        logger.error(
            'HTTP error occurred',
            http_error=str(http_exception),
            endpoint=url,
            data_from_user=from_user_data,
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
            data_from_user=from_user_data,
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exception),
        )
    
    if response.status_code == 403:
        logger.error(
            'User is blocked',
            status_code=response.status_code,
            reason=response.reason,
            response=response.text,
        )

        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )
    
    if response.status_code != 200:
        logger.error(
            'Failed to get token', 
            status_code=response.status_code,
            reason=response.reason,
            response=response.text,
        )

        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()
        )
        
    if 'token' and 'telegram_id' not in response.json():
        logger.error(
            'No token or telegram_id in response',
            response=response.json(),
        )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid response from server'
        )
        
    logger.info(
        'Successfully retrieved token from Django server REST API',
        token=response.json().get('token'),
        telegram_id=response.json().get('telegram_id'),
        endpoint=url,
        data_from_user=from_user_data,
    )
        
    return TokenSchema.to_response(response.json())

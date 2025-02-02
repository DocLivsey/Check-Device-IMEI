from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
import structlog
import requests

logger = structlog.get_logger(__name__)

from settings import api_url_take_token, server_host, api_base_path, api_version
from v1.schemas.auth import TokenSchema, TelegramUserSchema, to_telegram_user, to_token

auth_router = APIRouter()


@auth_router.post(f'{api_url_take_token}', response_model=TokenSchema)
async def telegram_token_auth(from_user_data: dict):
    logger.info(
        'Handle POST request to API for Telegram token authentication with',
        data_from_user=from_user_data,
    )
    
    url = f'{server_host}{api_base_path}{api_version}{api_url_take_token}/'
    telegram_user: TelegramUserSchema
    response: requests.Response
    try:
        telegram_user = to_telegram_user(from_user_data)
        
        logger.debug(
            'Successfully mapping user data to TelegramUserSchema and trying to send request to Django server REST API endpoint',
            telegram_user=telegram_user.dict(),
            endpoint=url
        )

        response = requests.post(
            url=url,
            data=telegram_user.dict(),
        )
    except ValidationError as validation_error:
        logger.error(
            'Validation error occurred',
            validation_error=validation_error.json(),
            endpoint=url,
            data_from_user=from_user_data,
        )
        
        return {
            'status_code' : 404,
            'detail': str(validation_error)
        }
    except HTTPException as http_exception:
        logger.error(
            'HTTP error occurred',
            http_error=str(http_exception),
            endpoint=url,
            data_from_user=from_user_data,
        )
        
        return {
            'status_code' : http_exception.status_code,
            'detail': str(http_exception)
        }
    except Exception as exception:
        logger.error(
            'Exception occurred in sync process', 
            exc_info=exception,
            endpoint=url,
            data_from_user=from_user_data,
        )
        
        return {
            'status_code' : 400,
            'detail': str(exception)
        }
    
    if response.status_code != 200:
        logger.error(
            'Failed to get token', 
            status_code=response.status_code,
            reason=response.reason,
            response=response.text,
        )
        
        return {
            'status_code' : response.status_code,
            'detail': response.reason
        }
        
    if 'token' and 'telegram_id' not in response.json():
        logger.error(
            'No token or telegram_id in response',
            response=response.json(),
        )
        
        return {
            'status_code': 400,
            'detail': 'Invalid response from server'
        }
        
    logger.info(
        'Successfully retrieved token from Django server REST API',
        token=response.json().get('token'),
        telegram_id=response.json().get('telegram_id'),
        endpoint=url,
        data_from_user=from_user_data,
    )
        
    return to_token(response.json())

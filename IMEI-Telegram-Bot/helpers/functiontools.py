import requests
import structlog
from aiogram.types import Message

from settings import Settings

logger = structlog.get_logger(__name__)


def auth_required(users_tokens: dict, user_id: int, message: Message):
    logger.info(
        'requere authentication',
        for_user=user_id
    )
    
    try:
        authenticate(users_tokens, user_id)
        
        logger.info(
            'User authenticated',
            user_id=user_id
        )
        
    except Exception as exception:
        logger.error(
            'Failed to authenticate user',
            user_id=user_id,
            exception=str(exception),
        )
        
        message.answer('You are not authenticated')


def authenticate(users_tokens: dict, user_id: int):
    logger.info(
        'trying to authenticate user',
        user=user_id
    )
    
    if user_id not in users_tokens:
        
        logger.info(
            'user not cached yet, sending request to authenticate user',
            user=user_id,
        )
        
        users_tokens[user_id] = request_auth_token(user_id)
        
        logger.info(
            'User authenticated successfully',
            user=user_id,
            token=users_tokens[user_id]
        )
        
        return
    
    if not users_tokens[user_id]:
        logger.info(
            'user not authenticated, sending request to authenticate user',
            user=user_id
        )
        
        users_tokens[user_id] = request_auth_token(user_id)
        
        logger.info(
            'User authenticated successfully',
            user=user_id,
            token=users_tokens[user_id]
        )
        
        return
    
    return


def request_auth_token(user_id: int) -> str:
    url = f'{Settings.API_HOST}{Settings.API_BASE_PATH}{Settings.API_VERSION}{Settings.API_URL_TAKE_TOKEN}'
    
    try:
        logger.info(
            'sending request to API to get token',
            api_url=url,
            user=user_id,
        )
        
        response = requests.post(
                url=url,
            )
        
    except requests.RequestException as http_error:
        logger.error(
            'Failed to send request',
            status_code=http_error.status_code,
            reason=http_error.reason,
        )
        
        raise Exception('Not Authenticated')
        
    if response.status_code != 200:
        logger.error(
            'Failed to get token', 
            status_code=response.status_code,
            reason=response.reason,
            response=response.text,
        )
        
        raise Exception('Not Authenticated')
    
    if 'token' not in response.json():
        logger.error(
            'No token in response',
            response=response.json(),
        )
        
        raise Exception('Not Authenticated')
        
    return response.json()['token']

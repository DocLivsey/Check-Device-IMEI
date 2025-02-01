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
            exception=exception.with_traceback(),
        )
        
        message.answer('You are not authenticated')


def authenticate(users_tokens: dict, user_id: int):
    logger.info(
        'tring to authenticate user',
        user=user_id
    )
    
    if not users_tokens[user_id]:
        logger.info(
            'user not authenticated, sending request to authenticate user',
            user=user_id
        )
        
        response = requests.post(
            url=f'{Settings.API_HOST}{Settings.API_BASE_PATH}{Settings.API_VERSION}{Settings.API_URL_TAKE_TOKEN}',
        )
        if response.status_code != 200:
            logger.error(
                'Failed to get token', 
                response=response
            )
            
            raise Exception('Not Authenticated')
        
        users_tokens[user_id] = response.json()['token']
        
        logger.info(
            'User authenticated successfully',
            user=user_id,
            token=users_tokens[user_id]
        )
        
        return
    
    return
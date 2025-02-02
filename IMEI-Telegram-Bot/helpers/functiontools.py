import requests
import structlog
from aiogram.types import Message, User
from pydantic import ValidationError

from schemas.auth import TelegramUserSchema, to_telegram_user, TokenSchema, to_token, from_telegram_user
from settings import api_host, api_base_path, api_version, api_auth_url, api_url_take_token

logger = structlog.get_logger(__name__)


async def auth_required(users_tokens: dict, user: User, message: Message):
    user_id: int = user.id

    logger.info(
        'requere authentication',
        for_user=user_id
    )
    
    try:
        authenticate(users_tokens, user)
        
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
        
        await message.answer('You are not authenticated')


def authenticate(users_tokens: dict, user: User):
    user_id: int = user.id

    logger.info(
        'trying to authenticate user',
        user=user_id
    )
    
    if user_id not in users_tokens:
        
        logger.info(
            'user not cached yet, sending request to authenticate user',
            user=user_id,
        )
        
        users_tokens[user_id] = request_auth_token(user).token
        
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
        
        users_tokens[user_id] = request_auth_token(user).token
        
        logger.info(
            'User authenticated successfully',
            user=user_id,
            token=users_tokens[user_id]
        )
        
        return
    
    return


def request_auth_token(user: User) -> TokenSchema:
    url = f'{api_host}{api_base_path}{api_version}{api_auth_url}{api_url_take_token}'
    user_id = user.id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    response: requests.Response
    telegram_user: TelegramUserSchema
    try:
        telegram_user = to_telegram_user(
            {
                'telegram_id': user_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        logger.info(
            'sending request to API to get token with data',
            api_url=url,
            user=user_id,
            data=from_telegram_user(telegram_user)
        )
        
        response = requests.post(
            url=url,
            data=from_telegram_user(telegram_user)
        )
        
    except requests.RequestException as http_error:
        logger.error(
            'Failed to send request',
            http_error=str(http_error),
        )
        
        raise Exception('Not Authenticated')

    except ValidationError as validation_error:
        logger.error(
            'Failed to mapping from object to DTO',
            validation_error=str(validation_error),
            data={
                'telegram_id': user_id,
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
            }
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

    users_token: TokenSchema
    try:
        users_token = to_token(response.json())
    except ValidationError as validation_error:
        logger.error(
            'Failed to mapping from object to DTO',
            validation_error=str(validation_error),
            data=response.json(),
        )

        raise Exception('Not Authenticated')
        
    return users_token

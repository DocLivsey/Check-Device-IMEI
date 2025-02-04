import requests
import structlog
from aiogram.types import Message

from schemas.auth import UserStatus
from settings import api_host, api_base_path, api_version

logger = structlog.get_logger(__name__)


async def start_handler_logic(
        message: Message,
        token: str | UserStatus,
):
    url = f'{api_host}{api_base_path}{api_version}/check-imei/hello/'

    logger.info(
        'starting work of `start_handler` logic'
        'Trying to send request to API to get welcome message',
        token=token,
        url=url,
    )
    
    if token == UserStatus.BLOCKED:
        logger.error(
            'User was blocked'
        )
        
        message_text = 'You are not allowed to perform this action because you was been blocked'
        
        await message.answer(message_text)
        return

    response: requests.Response
    try:
        response = requests.get(
            url=url,
            headers={
                'Authorization': f'Token {token}'
            }
        )
    except requests.RequestException as request_exception:
        logger.error(
            'Failed to get welcome message from API',
            token=token,
            exception=str(request_exception),
        )

        message_text = 'Something went wrong. Please try again later.'

        await message.answer(message_text)
        return
        
    if response.status_code == 401:
        logger.error(
            'Authentication failed',
            token=token,
        )
        
        message_text = 'You are not authorized to perform this action'
        
        await message.answer(message_text)
        return
    
    if response.status_code == 403:
        return
        
    if 'message' not in response.json():
        logger.error(
            'No message received from API',
            token=token,
        )
        
        message_text = 'Who are you?'
        
        await message.answer(message_text)
        return
        

    message_text = response.json().get('message')

    await message.answer(message_text)
    return


async def help_handler_logic(message: Message):
    await message.answer('hello')

from collections.abc import Callable

import requests
import structlog
from aiogram.types import Message

from settings import api_host, api_base_path, api_version

logger = structlog.get_logger(__name__)


def is_authenticated(users_tokens: dict, user_id: int) -> bool:
    return user_id in users_tokens and users_tokens[user_id] is not None


async def passed_auth_then_do(
        users_tokens: dict,
        user_id: int,
        handler: Callable,
        *args,
        **kwargs
):
    if is_authenticated(users_tokens, user_id):
        await handler(*args, **kwargs)

    else:
        return


async def start_handler_logic(
        message: Message,
        user_id: int,
        token: str,
):
    url = f'{api_host}{api_base_path}{api_version}/hello/'

    logger.info(
        'starting work of `start_handler` logic'
        'Trying to send request to API to get welcome message',
        token=token,
        user=user_id,
        url=url,
    )

    response: requests.Response
    message_text = 'Hello!'
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

    await message.answer(f'hello, {message.from_user}')


async def help_handler_logic(message: Message):
    await message.answer('hello')

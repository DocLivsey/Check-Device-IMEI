import requests
import structlog
from aiogram.types import Message

from helpers.functiontools import handle_401, handle_403
from schemas.auth import UserStatus
from settings import api_host, api_base_path, api_version

logger = structlog.get_logger(__name__)


async def check_imei_handler_logic(
        users_tokens: dict,
        message: Message,
        imei: str
):
    url = f'{api_host}{api_base_path}{api_version}/check-imei/'
    user_id = message.from_user.id
    token = users_tokens[user_id]

    logger.info(
        'Starting work of `start_handler` logic. '
        'Trying to send request to API to get welcome message',
        token=token,
        user=user_id,
        imei=imei,
        url=url,
    )

    # TODO: prevents rechecking the user's blocking, if the user is unbanned, the request is not sent anyway
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
            headers={'Authorization': f'Token {token}'},
            json={'imei': imei}
        )
    except requests.RequestException as request_exception:
        logger.error(
            f'Failed to check device imei from API',
            token=token,
            exception=str(request_exception),
        )

        response = request_exception.response

        await handle_401(message, response, token)
        await handle_403(message, response, token)

        message_text = 'Something went wrong. Please try again later.'

        await message.answer(message_text)
        return

    return

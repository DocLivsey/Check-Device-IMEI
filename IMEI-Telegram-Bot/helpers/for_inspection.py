import requests
import structlog
from aiogram.types import Message
from pydantic import ValidationError

from helpers.functiontools import handle_401, handle_403
from schemas.auth import UserStatus
from schemas.inspection import IMEICheckScheme, to_imei_check
from settings import api_host, api_base_path, api_version

logger = structlog.get_logger(__name__)
INVALID_MESSAGE = 'Invalid IMEI'


async def check_imei_handler_logic(
        users_tokens: dict,
        message: Message,
):
    url = f'{api_host}{api_base_path}{api_version}/check-imei/'
    user_id = message.from_user.id
    token = users_tokens[user_id]

    logger.info(
        'Starting work of `start_handler` logic. '
        'Trying to send request to API to get welcome message',
        token=token,
        user=user_id,
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

    message_text = (
        'Ok, if You want to check your device by IMEI, send me IMEI '
        '(it is a code consisting only of digits and 8 to 15 characters long).'
    )

    await message.answer(message_text)

    given_imei = message.text
    imei: str = validate_imei(given_imei)

    logger.info(
        'IMEI received from the user',
        user=user_id,
        imei=imei,
    )

    if imei == INVALID_MESSAGE:
        logger.error(
            'throw message that given IMEI is invalid',
            token=token,
            user=user_id,
            imei=imei,
        )

        message_text = f'Given IMEI ({given_imei}) is invalid'

        await message.answer(message_text)
        return

    response: requests.Response
    imei_response: IMEICheckScheme
    try:
        response = requests.get(
            url=url,
            headers={'Authorization': f'Token {token}'},
            json={'imei': imei}
        )

        response_data = response.json()
        imei_response = to_imei_check(response_data)
    except requests.RequestException as request_exception:
        logger.error(
            'Failed to check device imei from API',
            token=token,
            exception=str(request_exception),
        )

        response = request_exception.response

        await handle_401(message, response, token)
        await handle_403(message, response, token)

        message_text = 'Something went wrong. Please try again later.'

        await message.answer(message_text)
        return

    except ValidationError or TypeError as validation_error:
        logger.error(
            'Failed to mapping from request data to IMEI response scheme',
            user=user_id,
            imei=imei,
            response=str(validation_error),
        )

        message_text = 'Something went wrong. Please try again later or try another IMEI.'

        await message.answer(message_text)
        return

    except Exception as error:
        logger.error(
            'Something went wrong',
            user=user_id,
            imei=imei,
            error=str(error),
        )

        message_text = 'Something went wrong. Please try again later or try another IMEI.'

        await message.answer(message_text)
        return

    message_text = (
        f'''
        imei: {imei_response.device_id}
        '''
    )

    await message.answer(message_text)
    return


def is_valid_imei(imei: str) -> bool:
    return imei.isdigit() and 8 <= len(imei) <= 15


def validate_imei_or_else_throw(imei: str, default: str=INVALID_MESSAGE) -> str:
    if not is_valid_imei(imei):
        logger.error(
            'Invalid imei, return default',
            imei=imei,
            default=default,
        )
        return default

    return imei


def validate_imei(imei: str) -> str:
    return validate_imei_or_else_throw(imei)


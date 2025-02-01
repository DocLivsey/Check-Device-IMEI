import requests
import structlog
from aiogram import Router, types
from aiogram.filters import Command

from settings import Settings
from helpers.decorators import bot_logger

logger = structlog.get_logger(__name__)
router = Router()


@bot_logger
@router.message(Command('check_imei'))
async def check_imei_handler(message: types.Message):
    response = requests.get(
        url=f'{Settings.API_HOST}{Settings.API_BASE_PATH}{Settings.API_VERSION}/hello/',
        headers={
            'Authorization': 'Token 1994b2e652bf40d047300d2928b740fa8afc94f5'
        }
    )

    logger.debug(
        'response is',
        response=response,
    )

    to_user = response.json().get('message')
    await message.answer(to_user)
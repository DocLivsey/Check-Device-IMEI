import requests
import structlog
from aiogram import Router, types
from aiogram.filters import Command

from helpers.for_inspection import check_imei_handler_logic
from helpers.functiontools import auth_required, passed_auth_then_do
from settings import api_host, api_base_path, api_version
from helpers.decorators import bot_logger

logger = structlog.get_logger(__name__)
router = Router()


@bot_logger
@router.message(Command('check_imei'))
async def check_imei_handler(
        message: types.Message,
        users_tokens: dict
):
    await auth_required(users_tokens, message.from_user, message)

    await passed_auth_then_do(
        users_tokens,
        message,
        check_imei_handler_logic
    )

import structlog
from aiogram import Router, types
from aiogram.filters import Command

from helpers.decorators import bot_logger
from helpers.for_greeting import start_handler_logic, help_handler_logic
from helpers.functiontools import auth_required, passed_auth_then_do

logger = structlog.get_logger(__name__)
router = Router()


@bot_logger
@router.message(Command('start'))
async def start_handler(
        message: types.Message,
        users_tokens: dict
):
    await auth_required(users_tokens, message.from_user, message)

    await passed_auth_then_do(
        users_tokens,
        message.from_user.id,
        start_handler_logic,
        message=message,
        token=users_tokens[message.from_user.id],
    )



@bot_logger
@router.message(Command('help'))
async def help_handler(
        message: types.Message,
        users_tokens: dict
):
    await auth_required(users_tokens, message.from_user, message)

    await passed_auth_then_do(
        users_tokens,
        message.from_user.id,
        help_handler_logic,
        message=message,
    )

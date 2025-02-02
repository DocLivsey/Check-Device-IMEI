import structlog
from aiogram import Router, types
from aiogram.filters import Command

from helpers.decorators import bot_logger
from helpers.functiontools import auth_required

logger = structlog.get_logger(__name__)
router = Router()


@bot_logger
@router.message(Command('start'))
async def start_handler(
        message: types.Message,
        users_tokens: dict
):
    await auth_required(users_tokens, message.from_user, message)
        
    await message.answer(f'hello, {message.from_user}')


@bot_logger
@router.message(Command('help'))
async def help_handler(
        message: types.Message,
        users_tokens: dict
):
    await message.answer('hello')

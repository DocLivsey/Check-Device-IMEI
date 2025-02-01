import structlog
from aiogram import Router, types
from aiogram.filters import Command

from settings import Settings
from helpers.decorators import bot_logger

logger = structlog.get_logger(__name__)
router = Router()


@bot_logger
@router.message(Command('start'))
async def start_handler(message: types.Message):
    await message.answer(f'hello, {message.from_user}')


@bot_logger
@router.message(Command('help'))
async def help_handler(message: types.Message):
    await message.answer('hello')

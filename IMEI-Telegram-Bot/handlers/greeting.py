import structlog
from aiogram import Router, types

from settings import Settings
from helpers.decorators import bot_logger

logger = structlog.get_logger(__name__)
router = Router()


@bot_logger
@router.message()
async def start(message: types.Message):
    await message.answer('hello')

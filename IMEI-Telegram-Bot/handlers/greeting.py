import structlog
from aiogram import Router, types

from settings import Settings

logger = structlog.get_logger(__name__)
router = Router()


@router.message()
async def start(message: types.Message):
    await message.answer('hello')

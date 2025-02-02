import structlog
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from settings import telegram_bot_token
from helpers.decorators import bot_logger
from handlers.greeting import router as greeting_router
from handlers.verification import router as verification_router

logger = structlog.get_logger(__name__)

bot_token = str(telegram_bot_token)
check_imei_bot = Bot(token=bot_token)
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)


@bot_logger
async def run():
    """
    Main loop functions for polling telegram bot
    """
    dispatcher.include_routers(
        greeting_router,
        verification_router
    )

    await check_imei_bot.delete_webhook(
        drop_pending_updates=True
    )

    await dispatcher.start_polling(
        check_imei_bot,
        users_tokens={}
    )



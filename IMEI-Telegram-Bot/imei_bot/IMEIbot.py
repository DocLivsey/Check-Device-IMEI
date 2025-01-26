import structlog
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from settings import Settings

logger = structlog.get_logger(__name__)

bot_token = Settings.TELEGRAM_BOT_TOKEN_KEY.value
check_imei_bot = Bot(token=bot_token)
storage = MemoryStorage()
dispatcher = Dispatcher(storage=storage)


async def run():
    """
    Main loop functions for polling telegram bot
    """
    await check_imei_bot.delete_webhook(
        drop_pending_updates=True
    )

    await dispatcher.start_polling(
        check_imei_bot,
    )



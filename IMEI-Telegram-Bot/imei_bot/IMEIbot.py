import structlog
from aiogram import Bot

from settings import Settings

logger = structlog.get_logger(__name__)

bot_token = Settings.TELEGRAM_BOT_TOKEN_KEY.value
imei_bot = Bot(token=bot_token)

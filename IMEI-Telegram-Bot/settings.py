from os import environ
from enum import Enum

import structlog

logger = structlog.get_logger(__name__)


class Settings(Enum):
    TELEGRAM_BOT_TOKEN_KEY = environ.get('TELEGRAM_BOT_TOKEN_KEY', None)
    API_TOKEN = environ.get('API_TOKEN', None)
    API_URL = environ.get('API_URL', None)
    API_BASE_PATH = environ.get('API_BASE_PATH', None)
    API_VERSION = environ.get('API_VERSION', None)

    @staticmethod
    def to_string():
        string = ', '.join(f'{var.name} = {var.value}' for var in Settings)
        return f'({string})'

logger.info(
    'read environment variables',
    settings=Settings.to_string()
)

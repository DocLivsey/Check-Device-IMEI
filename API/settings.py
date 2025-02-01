from os import environ
from enum import Enum

import structlog

logger = structlog.get_logger(__name__)


class Settings(Enum):
    SERVER_HOST = environ.get('API_URL', 'http://192.168.0.107:8000')
    API_BASE_PATH = environ.get('API_BASE_PATH', '/api')
    API_VERSION = environ.get('API_VERSION', '/v1')
    API_URL_TAKE_TOKEN = environ.get('API_TAKE_TOKEN_URL', '/api-token-telegram-auth/')

    @staticmethod
    def to_string():
        string = ', '.join(f'{var.name} = {var.value}' for var in Settings)
        return f'({string})'

logger.info(
    'read environment variables',
    settings=Settings.to_string()
)

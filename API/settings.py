from os import environ
from enum import Enum

import structlog

logger = structlog.get_logger(__name__)


class Settings(Enum):
    SERVER_HOST = environ.get('SERVER_HOST', 'http://192.168.0.107:8000')
    API_BASE_PATH = environ.get('API_BASE_PATH', '/api')
    API_VERSION = environ.get('API_VERSION', '/v1')
    API_AUTH_URL = environ.get('API_AUTH_URL', '/auth')
    API_URL_TAKE_TOKEN = environ.get('API_TAKE_TOKEN_URL', '/api-token-telegram-auth/')

    @staticmethod
    def to_string():
        string = ', '.join(f'{var.name} = {var.value}' for var in Settings)
        return f'({string})'

logger.info(
    'read environment variables',
    settings=Settings.to_string()
)

server_host = Settings.SERVER_HOST.value
api_base_path = Settings.API_BASE_PATH.value
api_version = Settings.API_VERSION.value
api_auth_url = Settings.API_AUTH_URL.value
api_url_take_token = Settings.API_URL_TAKE_TOKEN.value

if 'http' not in server_host:
    server_host = 'http://' + server_host

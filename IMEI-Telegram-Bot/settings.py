from os import environ
from enum import Enum


class Settings(Enum):
    TELEGRAM_BOT_TOKEN_KEY = environ.get('TELEGRAM_BOT_TOKEN_KEY', None)
    API_TOKEN = environ.get('API_TOKEN', None)
    API_URL = environ.get('API_URL', None)
    API_BASE_PATH = environ.get('API_BASE_PATH', None)
    API_VERSION = environ.get('API_VERSION', None)
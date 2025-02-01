import requests
import structlog

from settings import Settings

logger = structlog.get_logger(__name__)


def auth_required(users_tokens: dict, user_id: int):
    if not users_tokens[user_id]:
        response = requests.post(
            url=f'{Settings.API_HOST}{Settings.API_BASE_PATH}{Settings.API_VERSION}{Settings.API_URL_TAKE_TOKEN}',
        )
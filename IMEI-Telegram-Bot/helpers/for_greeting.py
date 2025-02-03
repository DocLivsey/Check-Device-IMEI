import structlog

logger = structlog.get_logger(__name__)


def is_authenticated(users_tokens: dict, user_id: int) -> bool:
    return user_id in users_tokens and users_tokens[user_id] is not None


def passed_auth_then_do():
    pass


def start_handler_():
    pass

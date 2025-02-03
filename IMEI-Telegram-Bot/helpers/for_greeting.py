from collections.abc import Callable

import structlog

logger = structlog.get_logger(__name__)


def is_authenticated(users_tokens: dict, user_id: int) -> bool:
    return user_id in users_tokens and users_tokens[user_id] is not None


def passed_auth_then_do(
        users_tokens: dict,
        user_id: int,
        handler: Callable,
        *args,
        **kwargs
):
    if is_authenticated(users_tokens, user_id):
        handler(users_tokens, *args, **kwargs)

    else:
        return


def start_handler_logic():
    pass

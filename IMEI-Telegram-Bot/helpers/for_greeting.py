from collections.abc import Callable

import structlog
from aiogram.types import Message

logger = structlog.get_logger(__name__)


def is_authenticated(users_tokens: dict, user_id: int) -> bool:
    return user_id in users_tokens and users_tokens[user_id] is not None


async def passed_auth_then_do(
        users_tokens: dict,
        user_id: int,
        handler: Callable,
        *args,
        **kwargs
):
    if is_authenticated(users_tokens, user_id):
        await handler(users_tokens, *args, **kwargs)

    else:
        return


async def start_handler_logic(message: Message):
    await message.answer(f'hello, {message.from_user}')

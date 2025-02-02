from pydantic import BaseModel


class TelegramUserSchema(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    last_name: str


class TokenSchema(BaseModel):
    token: str
    user: TelegramUserSchema


def to_telegram_user(telegram_user_data: dict) -> TelegramUserSchema:
    telegram_id = telegram_user_data.get('telegram_id') if 'telegram_id' in telegram_user_data else -1
    username = telegram_user_data.get('username') if 'username' in telegram_user_data else 'Undefined'
    first_name = telegram_user_data.get('first_name') if 'first_name' in telegram_user_data else 'Undefined'
    last_name = telegram_user_data.get('last_name') if 'last_name' in telegram_user_data else 'Undefined'

    if not telegram_id:
        telegram_id = -1

    if not username:
        username = 'Undefined'

    if not first_name:
        first_name = 'Undefined'

    if not last_name:
        last_name = 'Undefined'

    return TelegramUserSchema(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )


def from_telegram_user(telegram_user_schema: TelegramUserSchema) -> dict:
    return {
        'telegram_id': str(telegram_user_schema.telegram_id),
        'username': str(telegram_user_schema.username),
        'first_name': str(telegram_user_schema.first_name),
        'last_name': str(telegram_user_schema.last_name),
    }


def to_token(token_data: dict) -> TokenSchema:
    token = token_data.get('token') if 'token' in token_data else 'Undefined'
    user = token_data.get('user') if 'user' in token_data else {}

    if not token:
        token = 'Undefined'

    if not user:
        user = {}

    return TokenSchema(
        token=token,
        user=to_telegram_user(user),
    )


def from_token(token_schema: TokenSchema) -> dict:
    return {
        'token': token_schema.token,
        'user': token_schema.user,
    }

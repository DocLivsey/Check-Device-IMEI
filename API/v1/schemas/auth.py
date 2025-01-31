from pydantic import BaseModel


class TelegramUser(BaseModel):
    id: int
    username: str


class TelegramUserSchema(BaseModel):
    telegram_user: TelegramUser


class TokenSchema(BaseModel):
    token: str
    user: TelegramUserSchema

from pydantic import BaseModel


class TelegramUser(BaseModel):
    id: int
    username: str


class TelegramUserSchema(BaseModel):
    telegram_user: TelegramUser


class Token(BaseModel):
    token: str
    user: TelegramUserSchema

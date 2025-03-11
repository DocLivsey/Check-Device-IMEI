from pydantic import BaseModel


class TelegramUserSchema(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    last_name: str

    @staticmethod
    def to_scheme(data: dict):
        return TelegramUserSchema(**data)
    

class TokenSchema(BaseModel):
    token: str
    user: TelegramUserSchema

    @staticmethod
    def to_scheme(data: dict):
        return TokenSchema(**data)

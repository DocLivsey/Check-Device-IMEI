from typing import Dict

from pydantic import BaseModel


class TelegramUserSchema(BaseModel):
    telegram_id: int
    username: str
    first_name: str
    last_name: str
    

class TokenSchema(BaseModel):
    token: str
    user: TelegramUserSchema
    
    
def to_telegram_user(telegram_user_data: Dict) -> TelegramUserSchema:
    telegram_id = telegram_user_data.get('telegram_id') if 'telegram_id' in telegram_user_data else -1
    
    return TelegramUserSchema(
        telegram_id=telegram_id,
    )

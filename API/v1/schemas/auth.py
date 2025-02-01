from pydantic import BaseModel


class TelegramUserSchema(BaseModel):
    id: int
    username: str
    

class TokenSchema(BaseModel):
    token: str
    user: TelegramUserSchema
    
    
def to_telegram_user():
    pass

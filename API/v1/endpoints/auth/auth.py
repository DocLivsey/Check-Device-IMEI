from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.post('/api-token-telegram-auth/', response_model=None)
async def telegram_token_auth():
    pass

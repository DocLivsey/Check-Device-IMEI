from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
import requests

from settings import Settings
from v1.schemas.auth import TokenSchema, TelegramUserSchema, to_telegram_user

auth_router = APIRouter()


@auth_router.post(f'{Settings.API_URL_TAKE_TOKEN}', response_model=TokenSchema)
async def telegram_token_auth(from_user_data: dict):
    telegram_user: TelegramUserSchema
    try:
        telegram_user = to_telegram_user(from_user_data)

        response = requests.post(
            url=f'{Settings.SERVER_HOST}{Settings.API_BASE_PATH}{Settings.API_VERSION}{Settings.API_URL_TAKE_TOKEN}',
            data=telegram_user.dict(),
        )
    except ValidationError as validation_error:
        return {
            'status_code' : 404,
            'detail': str(validation_error)
        }
    except HTTPException as http_exception:
        return {
            'status_code' : http_exception.status_code,
            'detail': str(http_exception)
        }
    except Exception as exception:
        return {
            'status_code' : 400,
            'detail': str(exception)
        }

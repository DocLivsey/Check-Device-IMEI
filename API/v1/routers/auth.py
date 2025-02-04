from fastapi import APIRouter

from v1.endpoints.auth.auth import auth_router as auth_endpoints
from v1.schemas.auth import TokenSchema
from settings import api_auth_url

router = APIRouter()

router.include_router(
    auth_endpoints,
    prefix=str(api_auth_url),
    tags=["auth"],
    responses={
        500: {"description": "Internal Server Error"},
        404: {"description": "Not found"},
        403: {"description": "Forbidden"},
        401: {"description": "Not authorized"},
        400: {"description": "Bad Request"},
        200: {"token": TokenSchema}
    },
)

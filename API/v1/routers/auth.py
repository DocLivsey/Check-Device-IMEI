from fastapi import APIRouter

from v1.endpoints.auth.auth import auth_router as auth_endpoints

router = APIRouter()

router.include_router(
    auth_endpoints,
    prefix="/auth",
    tags=["auth"],
    responses={
        500: {"description": "Internal Server Error"},
        404: {"description": "Not found"},
        403: {"description": "Not authorized"},
    },
)

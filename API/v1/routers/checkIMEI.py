from fastapi import APIRouter

from v1.endpoints.check_imei.checkIMEI import check_imei_router as check_imei_endpoints
from v1.schemas.checkIMEI import IMEICheckScheme

router = APIRouter()

router.include_router(
    check_imei_endpoints,
    prefix="/check-imei",
    tags=["Check IMEI"],
    responses={
        500: {"description": "Internal Server Error"},
        429: {"description": "Too many requests. Please try again later"},
        422: {'description': 'Request data validation error'},
        404: {"description": "Not found"},
        403: {"description": "Forbidden"},
        402: {'description': 'Your account balance is insufficient for this order'},
        401: {"description": "Not authorized"},
        400: {"description": "Bad Request"},
        200: {'description': IMEICheckScheme},
    },
)

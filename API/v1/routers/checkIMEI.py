from fastapi import APIRouter

from v1.endpoints.check_imei.checkIMEI import check_imei_router as check_imei_endpoints

router = APIRouter()

router.include_router(
    check_imei_endpoints,
    prefix="/check-imei",
    tags=["Check IMEI"],
    responses={
        500: {"description": "Internal Server Error"},
        404: {"description": "Not found"},
        403: {"description": "Not authorized"},
        400: {"description": "Bad Request"},
    },
)

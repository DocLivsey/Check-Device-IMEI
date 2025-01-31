from fastapi import APIRouter

from v1.routers.auth import router as auth_router
from v1.routers.checkIMEI import router as check_imei_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(check_imei_router)

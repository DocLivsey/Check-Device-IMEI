import structlog
from aiogram import Router

from settings import Settings

logger = structlog.get_logger(__name__)
router = Router()
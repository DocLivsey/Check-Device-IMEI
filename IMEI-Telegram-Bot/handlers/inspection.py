import requests
import structlog
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from helpers.for_inspection import check_imei_handler_begin_logic, check_imei_handler_ending_logic
from helpers.functiontools import auth_required, passed_auth_then_do
from imei_bot.bot_states import ChecksStates
from helpers.decorators import bot_logger

logger = structlog.get_logger(__name__)
router = Router()


@bot_logger
@router.message(Command('check_imei'))
async def check_imei_handler_begin(
        message: types.Message,
        users_tokens: dict,
        state: FSMContext
):
    await auth_required(users_tokens, message.from_user, message)

    await passed_auth_then_do(
        users_tokens,
        message,
        check_imei_handler_begin_logic
    )

    await state.set_state(ChecksStates.waiting)


@bot_logger
@router.message(F.text, ChecksStates.waiting)
async def check_imei_handler_ending(
        message: types.Message,
        users_tokens: dict
):
    await auth_required(users_tokens, message.from_user, message)

    await passed_auth_then_do(
        users_tokens,
        message,
        check_imei_handler_ending_logic
    )

from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters.state import StateFilter

from neuroBot.extensions import (
    bot_settings,
    get_start_button_inline_menu_for_video_generation,
)


video_generation_router: Router = Router(name=bot_settings.BOT_ROUTER_NAME_3)


@video_generation_router.message(
    StateFilter(None),
    F.text == bot_settings.BOT_ROUTER_REPLY_KB_NAME_3,
)
async def image_description_handler(messsage: Message):
    await messsage.answer(
        "Доступные варианты",
        reply_markup=get_start_button_inline_menu_for_video_generation,
    )

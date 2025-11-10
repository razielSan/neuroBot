import aiohttp
from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters.state import StateFilter

from neuroBot.extensions import (
    bot_settings,
    get_start_buttons_inline_menu_for_image_description,
)

image_description_router: Router = Router(name=bot_settings.BOT_ROUTER_NAME_1)


@image_description_router.message(
    StateFilter(None),
    F.text == bot_settings.BOT_ROUTER_REPLY_KB_NAME_1,
)
async def image_description_handler(
    messsage: Message,
    session: aiohttp.ClientSession,
):

    await messsage.answer(
        "Доступные варианты",
        reply_markup=get_start_buttons_inline_menu_for_image_description,
    )

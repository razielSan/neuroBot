import aiohttp
from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters.state import StateFilter

from neuroBot.extensions import (
    bot_settings,
    get_start_buttons_inline_menu_for_image_description,
)
from settings.response import messages


image_description_router: Router = Router(name=bot_settings.BOT_ROUTER_NAME_1)


@image_description_router.message(
    StateFilter(None),
    F.text == bot_settings.BOT_ROUTER_REPLY_KB_NAME_1,
)
async def image_description_handler(
    messsage: Message,
    session: aiohttp.ClientSession,
) -> None:
    """Возвращает инлайн кнопки источников описания изображения."""

    await messsage.answer(
        text=messages.OPTIONS_BOT_MESSAGE,
        reply_markup=get_start_buttons_inline_menu_for_image_description,
    )

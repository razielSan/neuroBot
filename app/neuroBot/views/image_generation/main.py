from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters.state import StateFilter

from neuroBot.extensions import bot_settings
from neuroBot.extensions import get_start_button_inline_menu_for_image_generation
from settings.response import messages


image_generation_router: Router = Router(name=bot_settings.BOT_ROUTER_NAME_2)


@image_generation_router.message(
    StateFilter(None),
    F.text == bot_settings.BOT_ROUTER_REPLY_KB_NAME_2,
)
async def image_generation_handler(messsage: Message):
    await messsage.answer(
        text=messages.OPTIONS_BOT_MESSAGE,
        reply_markup=get_start_button_inline_menu_for_image_generation,
    )

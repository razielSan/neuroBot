from aiogram import Router, F
from aiogram.filters.state import StateFilter
from aiogram.types import Message
import aiohttp

from neuroBot.extensions import bot_settings, get_start_button_neuroBot
from settings.response import messages

main_router: Router = Router(name=bot_settings.BOT_NAME)


@main_router.message(StateFilter(None), F.text == "/start")
async def main_handler(message: Message, session: aiohttp.ClientSession):
    await message.answer(
        text=messages.START_BOT_MESSAGE,
        reply_markup=get_start_button_neuroBot,
    )

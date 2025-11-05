from aiogram import Router, F
from aiogram.filters.state import StateFilter
from aiogram.types import Message
import aiohttp

from neuroBot.extensions import bot_settings, get_start_button_neuroBot

main_router: Router = Router(name=bot_settings.BOT_NAME)


@main_router.message(StateFilter(None), F.text == "/start")
async def main_handler(message: Message, session: aiohttp.ClientSession):
    await message.answer(
        text="Главное меню бота",
        reply_markup=get_start_button_neuroBot,
    )

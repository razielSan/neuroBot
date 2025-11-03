from aiogram import Router, F
from aiogram.filters.state import StateFilter
from aiogram.types import Message
import aiohttp

from neuroBot.extensions import bot_settings
from neuroBot.keyboards.reply.main import get_start_menu_button
from erros_handlers.main import error_handler_for_the_website
from neuroBot.extensions import error_logger

main_router: Router = Router(name=bot_settings.BOT_NAME)


@main_router.message(StateFilter(None), F.text == "/start")
async def main_handler(message: Message, session: aiohttp.ClientSession):
    data = await error_handler_for_the_website(
        session=session, 
        url="https://www.kinopoisk.ru/",
        error_logging=error_logger,
        name_router=f"{bot_settings.BOT_NAME}"
    )

    if data.error:
        await message.answer(
            text=data.error,
            reply_markup=get_start_menu_button(),
        )
    else:
        await message.answer(
            text=data.message,
            reply_markup=get_start_menu_button(),
        )
    # await message.answer(
    #     text="Главное меню бота",
    #     reply_markup=get_start_menu_button(),
    # )

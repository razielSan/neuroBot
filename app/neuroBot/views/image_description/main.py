import aiohttp
from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters.state import StateFilter

from neuroBot.extensions import bot_settings


image_description_router: Router = Router(name=bot_settings.BOT_ROUTER_NAME_1)


@image_description_router.message(StateFilter(None), F.text == "Описание Изображений")
async def image_description_handler(
    messsage: Message,
    session: aiohttp.ClientSession,
):
    await messsage.answer("image_description")

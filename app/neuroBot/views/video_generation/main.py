from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters.state import StateFilter

from neuroBot.extensions import bot_settings


video_generation_router: Router = Router(name=bot_settings.BOT_ROUTER_NAME_3)


@video_generation_router.message(StateFilter(None), F.text == "Генерация Видео")
async def image_description_handler(messsage: Message):
    raise ValueError
    await messsage.answer("video_generation")

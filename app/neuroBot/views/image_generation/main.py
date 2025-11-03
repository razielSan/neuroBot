from aiogram.types import Message
from aiogram import Router, F
from aiogram.filters.state import StateFilter

from neuroBot.extensions import bot_settings


image_generation_router: Router = Router(name=bot_settings.BOT_ROUTER_NAME_2)


@image_generation_router.message(StateFilter(None), F.text == "Генерация Изображений")
async def image_generation_handler(messsage: Message):
    raise UnboundLocalError
    await messsage.answer(text="image_generation")

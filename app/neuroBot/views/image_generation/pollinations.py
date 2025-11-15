from uuid import uuid4

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiohttp import ClientSession

from settings.response import messages
from neuroBot.extensions import (
    img_gen_pollinations_settings,
    neurobot_image_generation_logger,
)
from utils.network import get_and_save_image
from utils.filesistem import delete_data
from utils.keyboards_utils import get_reply_cancel_button
from neuroBot.extensions import bot, get_start_button_neuroBot
from core.response import ResponseData
from erros_handlers.decorator import safe_async_execution


router: Router = Router(name=img_gen_pollinations_settings.NAME_ROUTER)


class PollinationsImageGenerationFSM(StatesGroup):
    """FSM для генерации изображения для сайта  pollinations."""

    spam: State = State()
    description: State = State()


@router.callback_query(
    StateFilter(None),
    F.data == img_gen_pollinations_settings.CALLBACK_BUTTON_DATA,
)
async def pollinations(call: CallbackQuery, state: FSMContext) -> None:
    """
    Работа с FSM PollinationsImageGenerationFSM.

    Просит пользователя ввести описание ля изображения.
    """
    await call.message.edit_reply_markup(reply_markup=None)

    await call.message.answer(
        text=messages.IMAGE_DESCRIPTION_MESSAGE,
        reply_markup=get_reply_cancel_button(),
    )
    await state.set_state(PollinationsImageGenerationFSM.description)


@router.message(PollinationsImageGenerationFSM.description, F.text == "Отмена")
async def cancel_pollinations_img_gen_handler(
    message: Message, state: FSMContext
) -> None:
    """
    Работа с FSM ImaggaImgDescFSM.

    Отменяет все действияю
    """
    await state.clear()
    await message.answer(
        text=messages.CANCEL_MESSAGE,
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.START_BOT_MESSAGE,
        reply_markup=get_start_button_neuroBot,
    )


@router.message(PollinationsImageGenerationFSM.spam, F.text)
async def get_messge_from_img_gen_pollinations(
    message: Message, state: FSMContext
) -> None:
    """
    Работа с FSM PollinationsImageGenerationFSM.

    Отправлюяют пользователю сообщение при обработке запроса
    """
    await message.reply(text=messages.WAIT_MESSAGE)


@router.message(
    PollinationsImageGenerationFSM.description,
    F.text,
)
async def add_img(message: Message, state: FSMContext, session: ClientSession) -> None:
    """
    Работа с FSM PollinationsImageGenerationFSM.

    Отправляет пользователю сгенерированное изображение.
    """
    await state.set_state(PollinationsImageGenerationFSM.spam)

    await message.answer(
        text=messages.WAIT_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )

    path_img = None

    # Встаем в spam для ответа пользователю при запросе
    await state.set_state(PollinationsImageGenerationFSM.spam)

    # Формируем url для гегенрации изображения
    url: str = img_gen_pollinations_settings.IMAGE_GENERATE.format(
        text=message.text,
    )

    # Формируем имя изображения
    path_img: str = (
        img_gen_pollinations_settings.PATH_TO_POLLINATIONS_IMAGES_GENERATION
        / f"{uuid4().hex}.jpg"
    )

    # Оборочиваем get_and_save_image в декоратор для перехвата всех возможных ошибок
    decorator_function = await safe_async_execution(
        logging_data=neurobot_image_generation_logger
    )
    func = decorator_function(get_and_save_image)

    # Делаем заропс на получение картинки по описантю
    response_img: ResponseData = await func(
        data_requests=url,
        session=session,
        path_img=path_img,
        logging_data=neurobot_image_generation_logger,
    )

    if response_img.message:
        await state.clear()
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=FSInputFile(path=response_img.message),
        )
        await bot.send_message(
            chat_id=message.chat.id,
            text=messages.START_BOT_MESSAGE,
            reply_markup=get_start_button_neuroBot,
        )
    else:
        await state.set_state(PollinationsImageGenerationFSM.description)
        await message.answer(
            text=f"{response_img.error}\n{messages.TRY_REPSONSE_MESSAGE}",
            reply_markup=get_reply_cancel_button(),
        )
    if path_img:
        # Удаляет картинку
        delete_data(list_path=[path_img])

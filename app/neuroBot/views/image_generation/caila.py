from uuid import uuid4
from pathlib import Path
from typing import Dict

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from aiohttp import ClientSession
from utils.filesistem import delete_data

from neuroBot.extensions import (
    img_gen_caila_io_settings,
    neurobot_image_generation_logger,
    bot,
    get_start_button_neuroBot,
)
from utils.keyboards_utils import get_total_buttons_inline_kb, get_reply_cancel_button
from settings.response import messages
from core.config import InlineKeyboardData
from neuroBot.bot_functions.image_generation import get_url_video_generate_by_caila
from utils.network import get_and_save_image
from erros_handlers.decorator import safe_async_execution


router: Router = Router(name=img_gen_caila_io_settings.NAME_ROUTER)


class CailaImageGeneration(StatesGroup):
    """FSM для генерации изображений для сайта https://caila.io/."""

    spam: State = State()
    source: State = State()
    prompt: State = State()


@router.callback_query(
    StateFilter(None), F.data == img_gen_caila_io_settings.CALLBACK_BUTTON_DATA
)
async def caila(call: CallbackQuery, state: FSMContext) -> None:
    """Отправляет пользователю инлайн клавиатуру с выборами моделей."""
    # Удаляет инлайн клавиатуру
    await call.message.edit_reply_markup(reply_markup=None)

    await call.message.answer(
        text=messages.OPTIONS_BOT_MESSAGE,
        reply_markup=get_total_buttons_inline_kb(
            list_inline_kb_data=[
                InlineKeyboardData(
                    text=img_gen_caila_io_settings.MODEL_GPT_IMAGE_1_TEXT,
                    callback_data=img_gen_caila_io_settings.MODEL_GPT_IMAGE_1_DATA,
                ),
                InlineKeyboardData(
                    text=img_gen_caila_io_settings.MODEL_DALI_E_3_TEXT,
                    callback_data=img_gen_caila_io_settings.MODEL_DALI_E_3_DATA,
                ),
            ]
        ),
    )


@router.message(CailaImageGeneration.prompt, F.text == "Отмена")
async def cancel_handler_for_caila(message: Message, state: FSMContext) -> None:
    """Работа с FSM CailaImageGeneration.Отменяет все дейсвтия."""
    await state.clear()
    await message.answer(
        text=messages.CANCEL_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.START_BOT_MESSAGE,
        reply_markup=get_start_button_neuroBot,
    )


@router.message(CailaImageGeneration.spam, F.text)
async def get_message_for_caila(message: Message) -> None:
    """
    Работа с FSM CailaImageGeneration.Отправляет пользователю сообщение
    при вводе текста во время обработке запроса.
    """
    await message.reply(text=messages.WAIT_MESSAGE)


@router.callback_query(StateFilter(None), F.data.startswith("img_gen caila "))
async def add_source_caila(call: CallbackQuery, state: FSMContext) -> None:
    """Работа с FSM CailaImageGeneration.Просит пользователя ввести описание для изображения."""
    _, _, source = call.data.split(" ")

    await call.message.edit_reply_markup(reply_markup=None)

    # Добавляем модель генерации изображений
    await state.set_state(CailaImageGeneration.source)
    await state.update_data(source=source)

    await call.message.answer(
        text=messages.IMAGE_DESCRIPTION_MESSAGE,
        reply_markup=get_reply_cancel_button(),
    )
    await state.set_state(CailaImageGeneration.prompt)


@router.message(CailaImageGeneration.prompt, F.text)
async def add_prompt(
    message: Message,
    state: FSMContext,
    session: ClientSession,
) -> None:
    """
    Работа с FSM CailaImageGeneration. Отправляет сгенерированную картинку пользователю.
    """

    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.WAIT_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )
    # Встаем в состояние spam для отправки пользователю сообщеия при вводе текста
    # во время обработки запроса
    await state.set_state(CailaImageGeneration.spam)

    data: Dict = await state.get_data()
    source: str = data.get("source")

    # Формируем путь до картинки
    path_img: Path = (
        img_gen_caila_io_settings.PATH_TO_CAILA_IMAGES_GENERATION / f"{uuid4().hex}.jpg"
    )

    # Оборачиваем функцию в декоратор для отлова всех возможных ошибок
    decorator_function = await safe_async_execution(
        logging_data=neurobot_image_generation_logger,
    )
    func = decorator_function(get_url_video_generate_by_caila)

    # Получаем url или base64 изображения
    response_img = await func(
        url=img_gen_caila_io_settings.URL_IMAGE_GENERATE,
        api_key=img_gen_caila_io_settings.APIKEY_CAILA_IG,
        model=source,
        session=session,
        promtp=message.text,
        logging_data=neurobot_image_generation_logger,
    )

    if response_img.message:
        # Проверка на base64
        base_64: bool = (
            True
            if source == img_gen_caila_io_settings.MODEL_GPT_IMAGE_1_NAME
            else False
        )
        # Оборачиваем функцию в декоратор для отлова всех возможных ошибок
        decorator_function = await safe_async_execution(
            logging_data=neurobot_image_generation_logger,
        )
        func = decorator_function(get_and_save_image)

        img = await func(
            response_img.message,
            path_img,
            session,
            neurobot_image_generation_logger,
            base_64=base_64,
        )
        if img.message:
            await state.clear()
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=FSInputFile(path=img.message),
            )
            await bot.send_message(
                chat_id=message.chat.id,
                text=messages.START_BOT_MESSAGE,
                reply_markup=get_start_button_neuroBot,
            )
        else:
            await state.set_state(CailaImageGeneration.prompt)
            await message.answer(
                text=f"{response_img.error}\n{messages.TRY_REPSONSE_MESSAGE}",
                reply_markup=get_reply_cancel_button(),
            )

    else:
        await state.set_state(CailaImageGeneration.prompt)
        await message.answer(
            text=f"{response_img.error}\n{messages.TRY_REPSONSE_MESSAGE}",
            reply_markup=get_reply_cancel_button(),
        )
    # Удаляем изображение
    if path_img:
        delete_data(list_path=[path_img])

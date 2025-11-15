from uuid import uuid4
from pathlib import Path

import aiohttp
from aiogram.types import Message, CallbackQuery, ContentType, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from neuroBot.extensions import (
    img_desc_imagga_settings,
    bot,
    get_start_button_neuroBot,
    neurobot_image_description_logger,
)
from neuroBot.bot_functions.image_description import get_image_description_by_immaga
from utils.keyboards_utils import get_reply_cancel_button
from core.response import ResponseData
from settings.response import messages
from utils.filesistem import delete_data
from erros_handlers.decorator import safe_async_execution


router: Router = Router(name=img_desc_imagga_settings.NAME_ROUTER)


class ImaggaImgDescFSM(StatesGroup):
    """FSM для описания изображений сайта immaga."""

    spam: State = State()
    prompt: State = State()


@router.callback_query(
    StateFilter(None),
    F.data == img_desc_imagga_settings.CALLBACK_BUTTON_DATA,
)
async def immaga(
    call: CallbackQuery,
    session: aiohttp.ClientSession,
    state: FSMContext,
) -> None:
    """Работа с FSM ImaggaImgDescFSM.Просит пользвателя скинуть картинку для анализа."""

    await call.message.edit_reply_markup(reply_markup=None)

    await call.message.answer(
        text=messages.DROP_PHOTO_MESSAGE,
        reply_markup=get_reply_cancel_button(),
    )

    await state.set_state(ImaggaImgDescFSM.prompt)


@router.message(ImaggaImgDescFSM.prompt, F.text == "Отмена")
async def cancel_imagga_img_desc_handler(message: Message, state: FSMContext) -> None:
    """Работа с FSM ImaggaImgDescFSM.Отменяет все действияю"""
    await state.clear()
    await message.answer(
        text=messages.CANCEL_MESSAGE,
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.START_BOT_MESSAGE,
        reply_markup=get_start_button_neuroBot,
    )


@router.message(ImaggaImgDescFSM.spam, F.text)
async def get_message_when_spam_for_imagga(message: Message, state: FSMContext) -> None:
    """
    Работа с FSM ImaggaImgDescFSM.
    Отправляет пользователю сообщение если был введен текс при обработке запроса.
    """

    await message.reply(text=messages.WAIT_MESSAGE)


@router.message(ImaggaImgDescFSM.prompt, F)
async def add_prompt_for_imagga(
    message: Message,
    session: aiohttp.ClientSession,
    state: FSMContext,
) -> None:
    """
    Работса с FSM ImaggaImgDescFSM.
    Отправляет пользователю анализ изображения.
    """

    if message.content_type == ContentType.PHOTO:
        path_img = None

        # Встаем в состояние spam для ответа пользователю при запросе
        await state.set_state(ImaggaImgDescFSM.spam)

        await message.answer(
            text=messages.WAIT_MESSAGE,
            reply_markup=ReplyKeyboardRemove(),
        )

        # Формируем путь для картинки
        path_img: Path = (
            img_desc_imagga_settings.PATH_TO_IMAGGA_IMAGES_DESCRIPTION
            / f"{uuid4().hex}.jpg"
        )
        # Скачиваем скиданную пользователем картинку для анализа
        await bot.download(file=message.photo[-1].file_id, destination=path_img)

        # Оборачиваем функцию в декоратор для отлавливания всех возможных ошибок
        decorator_function = await safe_async_execution(
            logging_data=neurobot_image_description_logger,
        )
        func = decorator_function(get_image_description_by_immaga)

        # Делаем запрос на получение описание изображения
        img_description: ResponseData = await func(
            key_autorization=img_desc_imagga_settings.ID_IMAGGA_AUTHORIZATION,
            upload_endpoint=img_desc_imagga_settings.UPLOAD_ENDPOINT,
            url_tags=img_desc_imagga_settings.URL_TAGS,
            path_img=path_img,
            session=session,
            logging_data=neurobot_image_description_logger,
            language="ru",
            limit=15,
        )
        if img_description.message:
            await state.clear()
            await message.answer(text=img_description.message)
            await bot.send_message(
                chat_id=message.chat.id,
                text="Главное меню бота",
                reply_markup=get_start_button_neuroBot,
            )
        else:

            await state.set_state(ImaggaImgDescFSM.prompt)
            await message.answer(
                text=f"{img_description.error}\n\n{messages.TRY_REPSONSE_MESSAGE}",
                reply_markup=get_reply_cancel_button(),
            )
        # Удаляем изоабражение
        if path_img:
            delete_data(
                list_path=[path_img],
                warning_logger=neurobot_image_description_logger.warning_logger,
            )

    else:
        await message.answer(
            text=messages.NOT_PHOTO_MESSAGE,
        )

import aiohttp
from uuid import uuid4
from aiogram.types import Message, CallbackQuery, ContentType, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from pathlib import Path


from neuroBot.extensions import (
    img_desc_imagga_settings,
    bot,
    bot_settings,
    image_description_error_logger,
    warning_logger,
    get_start_buttons_inline_menu_for_image_description,
    get_start_button_neuroBot,
)
from neuroBot.bot_functions.image_description import get_image_description_by_immaga
from utils.keyboards_utils import get_reply_cancel_button
from core.response import ResponseData
from settings.response import messages
from utils.filesistem import delete_data


imagga_img_desc_router: Router = Router(name=img_desc_imagga_settings.NAME_ROUTER)


class ImaggaImgDescFSM(StatesGroup):
    """FSM для описания изображений сайта immaga"""

    spam: State = State()
    prompt: State = State()


@imagga_img_desc_router.callback_query(
    StateFilter(None),
    F.data == img_desc_imagga_settings.CALLBACK_BUTTON_NAME,
)
async def immaga(
    call: CallbackQuery,
    session: aiohttp.ClientSession,
    state: FSMContext,
) -> None:

    await call.message.edit_reply_markup(reply_markup=None)

    await call.message.answer(
        "Скидывайте картинку для анализа",
        reply_markup=get_reply_cancel_button(),
    )

    await state.set_state(ImaggaImgDescFSM.prompt)


@imagga_img_desc_router.message(ImaggaImgDescFSM.prompt, F.text == "Отмена")
async def cancel_imagga_img_desc_handler(message: Message, state: FSMContext) -> None:
    """Работа с FSM ImgDescFS.Отменяет все действияю"""
    await state.clear()
    await message.answer(
        text="Запрос прерван.Описание изображений(imagga) отменено",
        reply_markup=get_start_button_neuroBot,
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="Доступные варианты",
        reply_markup=get_start_buttons_inline_menu_for_image_description,
    )


@imagga_img_desc_router.message(ImaggaImgDescFSM.spam, F.text)
async def get_message_when_spam_for_imagg(message: Message, state: FSMContext):
    await message.reply(text=messages.WAIT_MESSAGE)


@imagga_img_desc_router.message(ImaggaImgDescFSM.prompt, F)
async def add_prompt(
    message: Message,
    session: aiohttp.ClientSession,
    state: FSMContext,
) -> None:
    if message.content_type == ContentType.PHOTO:

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

        # Делаем запрос на получение описание изображения
        img_description: ResponseData = await get_image_description_by_immaga(
            key_autorization=img_desc_imagga_settings.ID_IMAGGA_AUTHORIZATION,
            upload_endpoint=img_desc_imagga_settings.UPLOAD_ENDPOINT,
            url_tags=img_desc_imagga_settings.URL_TAGS,
            path_img=path_img,
            session=session,
            error_logging=image_description_error_logger,
            name_router=bot_settings.BOT_LOGGING_ERROR_NAME_1,
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
            # Удаляем изоабражение
            delete_data(
                path=path_img,
                warning_logger=warning_logger,
            )
        else:
            await state.set_state(ImaggaImgDescFSM.prompt)
            await message.answer(
                text=f"{img_description.error}\n\nСкидывайте, снова , картинку для анализа",
                reply_markup=get_reply_cancel_button(),
            )

    else:
        await message.answer(
            "Скидывамые данные должы быть фото в формате jpg,"
            " png или gif\n\nСкидывайте, снова , картинку для анализа",
        )

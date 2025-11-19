import asyncio
from uuid import uuid4
from typing import Dict
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter
from aiohttp import ClientSession

from neuroBot.extensions import (
    img_gen_stablehorde_settings,
    get_start_button_neuroBot,
    bot,
    neurobot_image_generation_logger,
)
from settings.response import messages
from utils.keyboards_utils import get_reply_cancel_button
from neuroBot.bot_functions.image_generation import (
    get_an_image_id_by_stablehorde,
    check_status_without_images_by_stablehorde,
)
from erros_handlers.decorator import safe_async_execution
from utils.fsm_utils import async_make_update_progress
from utils.chek_utils import checking_base64
from utils.network import get_and_save_image
from utils.filesistem import delete_data
from core.response import ResponseData


router: Router = Router(
    name=img_gen_stablehorde_settings.NAME_ROUTER,
)


class StablehordeImgGenFSM(StatesGroup):
    """FSM для генерации изображений сайта https://stablehorde.net."""

    data_state: State = State()
    cancel: State = State()
    prompt: State = State()


@router.callback_query(
    StateFilter(None),
    F.data == img_gen_stablehorde_settings.CALLBACK_BUTTON_DATA,
)
async def stablehorde(
    call: CallbackQuery,
    state: FSMContext,
) -> None:
    """
    Работа с FSM StablehordeImgGenFSM.

    Просит пользователя ввести описание изображения.

    Args:
        call (CallbackQuery): _description_
        state (FSMContext): _description_
    """
    # Удаляет инлайн клавиатуру
    await call.message.edit_reply_markup(reply_markup=None)

    await call.message.answer(
        text=messages.IMAGE_DESCRIPTION_MESSAGE,
        reply_markup=get_reply_cancel_button(),
    )

    await state.set_state(StablehordeImgGenFSM.prompt)


@router.message(StablehordeImgGenFSM.prompt, F.text == "Отмена")
@router.message(StablehordeImgGenFSM.data_state, F.text == "Отмена")
async def cancel_pollinations_img_gen_handler(
    message: Message, state: FSMContext
) -> None:
    """
    Работа с FSM StablehordeImgGenFSM.

    Отменяет все действияю
    """

    current_state = await state.get_state()

    # Если пользователь нажал кнопку отмены при генерации изображения
    if current_state == "StablehordeImgGenFSM:data_state":
        # Встаем в состояние отмены
        await state.set_state(StablehordeImgGenFSM.cancel)
        await state.update_data(cancel=True)
        return

    await state.clear()
    await message.answer(
        text=messages.CANCEL_MESSAGE,
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.START_BOT_MESSAGE,
        reply_markup=get_start_button_neuroBot,
    )


@router.message(StablehordeImgGenFSM.data_state, F.text)
@router.message(StablehordeImgGenFSM.cancel, F.text)
async def get_message(message: Message, state: FSMContext) -> None:
    """
    Работа с FSM StablehordeImgGenFSM.

    Отправляет сообщение пользователю при вводе пользователем текста
    во время запроса
    """
    await message.reply(text=messages.WAIT_AND_CANCEL_MESSAGE)


@router.message(StablehordeImgGenFSM.prompt, F.text)
async def add_prompt(
    message: Message,
    state: FSMContext,
    session: ClientSession,
) -> None:
    """
    Работса с FSM StablehordeImgGenFSM.

    Отправляет пользователю сгенерированную картинку.
    """

    # Встаем в состояние data_state для отслеживание прогресса
    # и отправление пользователю сообщения при запросе
    await state.set_state(StablehordeImgGenFSM.data_state)
    await state.update_data(data_state=-1)

    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.WAIT_GENERATION_MESSAGE.format(start=30, end=10),
    )
    # Оборачиваем функцию в декоратор для отлова всех возможных ошибок
    decorator_func = safe_async_execution(
        logging_data=neurobot_image_generation_logger,
    )
    func = decorator_func(get_an_image_id_by_stablehorde)

    # Получаем id картинки
    img_id = await func(
        img_gen_stablehorde_settings.REQUESTS_TO_GENERATE_IMAGES,
        img_gen_stablehorde_settings.APIKEY_STABLEHORDE_IG,
        message.text,
        session,
        neurobot_image_generation_logger,
    )

    path_img = None

    if img_id.message:
        # id картинки
        job_id: str = img_id.message.get("id")

        # Функция для отслеживания прогреса
        update_progress = async_make_update_progress(
            state=state,
        )

        # Оборачиваем функцию в декоратор для отлова всех возможных ошибок
        decorator_function = safe_async_execution(
            logging_data=neurobot_image_generation_logger
        )
        func = decorator_function(check_status_without_images_by_stablehorde)

        # Создаем task. Делаем запросы в цикле пока не картинка не создастся
        task_progress = asyncio.create_task(
            func(
                img_gen_stablehorde_settings.APIKEY_STABLEHORDE_IG,
                img_gen_stablehorde_settings.REQUESTS_STATUS_CHECK_WITHOUT_IMAGES,
                job_id,
                session,
                neurobot_image_generation_logger,
                time_working=60,
                update_progress=update_progress,
            )
        )

        # Создаем сообщение для отправления сообщений пользователю во время запроса
        progress_message: Message = await message.answer(
            text=messages.IMAGE_GENERATION_MESSAGE.format(
                image_count="...",
            ),
        )
        end_time: int = 0
        while not task_progress.done():
            data: Dict = await state.get_data()

            # Если пользователь нажал кнопку отмены
            if data.get("cancel"):
                task_progress.cancel()

                # позволяем task завершится корректно
                try:
                    await task_progress
                except asyncio.CancelledError:
                    pass
                # Выходим из цикла
                break
            wait_time = data.get("data_state")
            try:
                if wait_time > -1:
                    if wait_time != end_time:
                        await progress_message.edit_text(
                            text=messages.IMAGE_GENERATION_MESSAGE.format(
                                image_count=wait_time
                            ),
                        )
            except Exception:
                pass
            end_time = wait_time
            await bot.send_chat_action(chat_id=message.chat.id, action="typing")
            await asyncio.sleep(5)

        img_status: ResponseData = await task_progress

        data = await state.get_data()

        # Если пользователь нажал кнопку отмены
        if data.get("cancel"):

            # Отправляем пользователю сообщение и убираем кнопку отмены
            await message.answer(
                text=messages.BUTTON_CANCEL_MESSAGE,
                reply_markup=ReplyKeyboardRemove(),
            )
            # Ждем окончания всех процессов
            while not task_progress.done():
                await asyncio.sleep(1)

            await state.clear()
            await bot.send_message(
                chat_id=message.chat.id, text=messages.CANCEL_MESSAGE
            )
            await bot.send_message(
                text=messages.START_BOT_MESSAGE,
                chat_id=message.chat.id,
                reply_markup=get_start_button_neuroBot,
            )

        else:
            if img_status.message:

                # Встаем в состоние отмены чтобы пользователь не мог нажать кнопку
                await state.set_state(StablehordeImgGenFSM.cancel)

                # Отправляем пользователю сообщение о завершении генерации
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=messages.IMAGE_GENERATION_MESSAGE_END,
                    reply_markup=ReplyKeyboardRemove(),
                )

                # Ждем пока не завершатся все процессы
                while not task_progress.done():
                    pass

                # Оборачиваем функцию в декоратор для отлова всех возможных ошибок
                decorator_function = safe_async_execution(
                    logging_data=neurobot_image_generation_logger
                )
                func = decorator_function(check_status_without_images_by_stablehorde)

                # Делаем запрос на получение данных о картинке
                img_content = await func(
                    img_gen_stablehorde_settings.APIKEY_STABLEHORDE_IG,
                    img_gen_stablehorde_settings.REQUESTS_FULL_STATUS_IMAGE_GENERATIONS,
                    job_id,
                    session,
                    neurobot_image_generation_logger,
                    full_status_url=True,
                )
                if img_content.message:
                    # Достаем данные о изображении
                    data_countent: str = img_content.message.get("generations")[0][
                        "img"
                    ]

                    # Проверяем является ли изображение формата base64
                    base_64: bool = True if checking_base64(data_countent) else False

                    # Вычисляем формат файла
                    format_file: str = "png" if base_64 else "webp"

                    # Формируем путь до изображения
                    path_img: Path = (
                        img_gen_stablehorde_settings.PATH_TO_STABLEHORDE_IMAGES_GENERATION
                        / f"{uuid4().hex}.{format_file}"
                    )

                    # Оборачиваем функцию в декоратор для отлова всех возможных ошибок
                    decorator_func = safe_async_execution(
                        logging_data=neurobot_image_generation_logger,
                    )
                    func = decorator_func(get_and_save_image)

                    # Сохраняем изображение
                    data: ResponseData = await get_and_save_image(
                        data_countent,
                        path_img,
                        session,
                        neurobot_image_generation_logger,
                        base_64,
                    )
                    if data.message:
                        await state.clear()
                        await bot.send_photo(
                            chat_id=message.chat.id,
                            photo=FSInputFile(
                                path=path_img,
                            ),
                        )
                        await bot.send_message(
                            text=messages.START_BOT_MESSAGE,
                            chat_id=message.chat.id,
                            reply_markup=get_start_button_neuroBot,
                        )
                    else:
                        await state.set_state(StablehordeImgGenFSM.prompt)
                        await bot.send_message(
                            chat_id=message.chat.id,
                            text=f"{data.error}\n{messages.TRY_REPSONSE_MESSAGE}",
                            reply_markup=get_reply_cancel_button(),
                        )
                else:
                    await state.set_state(StablehordeImgGenFSM.prompt)
                    await bot.send_message(
                        chat_id=message.chat.id,
                        text=f"{img_content.error}\n{messages.TRY_REPSONSE_MESSAGE}",
                        reply_markup=get_reply_cancel_button(),
                    )
            else:
                await state.set_state(StablehordeImgGenFSM.prompt)
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"{img_status.error}\n{messages.TRY_REPSONSE_MESSAGE}",
                    reply_markup=get_reply_cancel_button(),
                )

    else:
        await state.set_state(StablehordeImgGenFSM.prompt)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"{img_id.error}\n{messages.TRY_REPSONSE_MESSAGE}",
            reply_markup=get_reply_cancel_button(),
        )

    # Удаляем изображение
    if path_img:
        delete_data(
            list_path=[path_img],
            warning_logger=neurobot_image_generation_logger.warning_logger,
        )

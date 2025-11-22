from typing import Dict, Callable, Optional, List
import asyncio
from uuid import uuid4
from pathlib import Path
from asyncio import AbstractEventLoop

from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    ContentType,
    FSInputFile,
    ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter

from neuroBot.extensions import (
    model_settings,
    bot,
    get_start_button_neuroBot,
    neurobot_video_generation_logger,
)
from utils.keyboards_utils import get_reply_cancel_button, get_total_buttons_inline_kb
from core.config import InlineKeyboardData
from core.response import ResponseData
from settings.response import messages
from utils.fsm_utils import make_update_progress
from utils.filesistem import delete_data
from neuroBot.bot_functions.video_generation import create_video_by_is_vheer
from erros_handlers.format import format_message
from erros_handlers.helpers import run_safe_inf_executror

router: Router = Router(
    name=model_settings.video_gen_models.vheer.SERVICE_NAME,
)


class VheerVideoGenerationFSM(StatesGroup):
    """FSM для работы с генерацией видео для сайта https://vheer.com/."""

    counter_progress: State = State()  # Счетчик прогресса скачивания видео
    cancel: State = State()  # Отмена скачивания видео
    image: State = State()
    description: State = State()
    data_state: State = State()  # Для определния готовности описания изображения


@router.callback_query(
    StateFilter(None),
    F.data == model_settings.video_gen_models.vheer.CALLBACK_BUTTON_DATA,
)
async def vheer(call: CallbackQuery, state: FSMContext) -> None:
    """Отправляет пользователю инлайн клавиатуру с доступными вариантам генерации видео."""
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        text=messages.OPTIONS_BOT_MESSAGE,
        reply_markup=get_total_buttons_inline_kb(
            [
                InlineKeyboardData(
                    text="1⃣  По Описанию и Изображению",
                    callback_data="vg_vheer description",
                ),
                InlineKeyboardData(
                    text="2⃣  По Изображению", callback_data="vg_vheer image"
                ),
            ]
        ),
    )


@router.message(VheerVideoGenerationFSM.description, F.text == "Отмена")
@router.message(VheerVideoGenerationFSM.image, F.text == "Отмена")
async def cancel__vheer_video_generation_handler(
    message: Message, state: FSMContext
) -> None:
    """
    Работа с FSM VheerVideoGenerationFSM.

    Отменяет все действия.
    """
    await state.clear()
    await message.answer(text=messages.CANCEL_MESSAGE)
    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.START_BOT_MESSAGE,
        reply_markup=get_start_button_neuroBot,
    )


@router.message(VheerVideoGenerationFSM.counter_progress, F.text)
async def get_message_for_vheer_video_generation(
    message: Message, state: FSMContext
) -> None:
    """
    Работа с FSM VheerVideoGenerationFSM.

    Отправляет пользователю сообщение при когда идет обработка запроса
    """
    await message.reply(text=messages.WAIT_MESSAGE)


@router.callback_query(
    F.data.startswith("vg_vheer "),
)
async def start_vheer_video_generation(call: CallbackQuery, state: FSMContext) -> None:
    """
    Работа с FSM VheerVideoGenerationFSM.

    Отлавливает какой тип генерации выбрал пользователь с соответсвующими действиями
    """
    _, vheer_data = call.data.split(" ")

    await call.message.edit_reply_markup(reply_markup=None)

    # Отлавливаем тип какой генерации видео выбрал пользователья
    if vheer_data == "image":
        # Если по видео переходим сразу в следующую функцию
        await add_description_for_vheer(message=call.message, state=state)
        return
    elif vheer_data == "description":
        # Добавляем описание
        await state.set_state(VheerVideoGenerationFSM.description)
        await state.update_data(description=True)

        await call.message.answer(
            text=messages.IMAGE_DESCRIPTION_MESSAGE,
            reply_markup=get_reply_cancel_button(),
        )


@router.message(VheerVideoGenerationFSM.description, F.text)
async def add_description_for_vheer(message: Message, state: FSMContext) -> None:
    """
    Работа с FSM VheerVideoGenerationFSM.

    Просит пользователя скинуть изображение
    """
    data_vheer: Dict = await state.get_data()

    # Если пользователь выбрал генерацию по описанию и изображению
    if data_vheer.get("description", None):
        await state.update_data(description=message.text)

    await message.answer(
        text=messages.DROP_PHOTO_MESSAGE,
        reply_markup=get_reply_cancel_button(),
    )
    await state.set_state(VheerVideoGenerationFSM.image)


@router.message(VheerVideoGenerationFSM.image, F)
async def add_photo_for_vheer(message: Message, state: FSMContext):
    """
    Работа с FSM VheerVideoGenerationFSM.

    Отправляем пользоваетелю сгенерированное видео.
    """
    if message.content_type == ContentType.PHOTO:
        # Создаем переменные для путей чтобы в конце если они есть удалить видео и изображение
        video_path = None
        path_image = None

        await bot.send_message(
            chat_id=message.chat.id,
            text=messages.WAIT_GENERATION_MESSAGE.format(start=30, end=5),
            reply_markup=ReplyKeyboardRemove(),
        )
        vheer_data: Dict = await state.get_data()

        # Встаем в состояние counter_progress для отслеживания прогресса  скачивания
        await state.set_state(VheerVideoGenerationFSM.counter_progress)
        await state.update_data(counter_progress=0)

        # Создаем петлю
        loop: AbstractEventLoop = asyncio.get_event_loop()

        # Функция для отслеживания прогресса запроса пользователя
        progress_update: Callable = make_update_progress(loop=loop, state=state)

        # Получаем имя файла
        photo_phile = message.photo[-1]
        file_info = await bot.get_file(photo_phile.file_id)
        file_path: str = file_info.file_path
        _, file_name = file_path.split("/")

        # Путь до картинки
        path_image: Path = (
            model_settings.video_gen_models.vheer.PATH_TO_IMAGES / file_name
        )

        # Скачиваем картинку в путь
        await message.bot.download(
            file=message.photo[-1].file_id,
            destination=path_image,
        )

        # Формируем путь до видео файла
        video_path: Path = (
            model_settings.video_gen_models.vheer.PATH_TO_VIDEO / f"{uuid4().hex}.mp4"
        )

        # Если пользователь ввел описание по изображению указываем url сайта генератора описаний
        description_url: Optional[str] = (
            model_settings.video_gen_models.vheer.PROMPT_IMG_URL_BY_DESCRIBEPICTURE_CC
            if not vheer_data.get("description", None)
            else None
        )

        # Формируем prompt
        prompt: str = vheer_data.get("description", None) or "Картинка движется"

        progress_task = asyncio.create_task(
            run_safe_inf_executror(
                loop,
                create_video_by_is_vheer,
                model_settings.video_gen_models.vheer.VIDEO_URL,
                path_image,
                video_path,
                model_settings.video_gen_models.vheer.VIDEO_DATA,
                prompt,
                progress_update,
                neurobot_video_generation_logger,
                description_url,
                logging_data=neurobot_video_generation_logger,
            )
        )

        # Общее количество шагов необходимое для запроса
        total_step: int = model_settings.video_gen_models.vheer.TOTAL_STEP
        video_progress: int = 0
        current_step: int = 0  # текущий шаг

        # Определяем если пользователь ввел генерацию только по изображению
        # встаем в True
        description_image: bool = True if description_url else False

        # Формируем сообщение и отправляем пользовтелю с отслеживанием прогресса скачивания
        if description_image:
            # Если генерация видео по изображению
            progress_message: Message = await message.answer(
                text=messages.DESCRPIPTION_AND_VIDEO_GENERATION_MESSAGE.format(
                    description_count="", video_count=video_progress
                )
            )

        else:
            # Если генерация видео по описнию и изображению
            progress_message: Message = await message.answer(
                text=messages.VIDEO_GENERATION_MESSAGE.format(
                    video_count=video_progress
                ),
            )

        # Формиурем список для отслеживания прогресс при запроса на формирования описания
        list_progress: List = [".", "..", "...", "....", "...."]
        counter_description: int = 0  # счетчик для описания изображения

        # Встаем в цикл пока петля не завершится

        while not progress_task.done():
            # Делаем копию во избежания получения старых данных при сильной нагрузке
            data: Dict = dict(await state.get_data())

            counter: int = data["counter_progress"]

            # Если идет создание видео по изображению
            if description_image:
                gen_description = data.get("data_state", None)
                # Сообщение на случай если сайт по генерации описания выдал ошибку
                default_description: str = (
                    (
                        "🤷‍♀️ Сайт"
                        " по генерации описания выдал ошибку."
                        "Будет использовано стандартное описание"
                    )
                    if gen_description == "default_description"
                    else ""
                )
                if gen_description:  # Если описание сформировалось
                    if counter != current_step:
                        # Обновляем видео прогресс
                        video_progress = counter / total_step * 100
                        current_step = counter

                        msg = messages.DESCRIPTION_END_AND_VIDEO_GENERATION_MESSAGE.format(
                            video_count=video_progress
                        )
                        await progress_message.edit_text(
                            text=f"{msg}\n{default_description}"
                        )

                else:  # Если описание не сформировалось
                    try:
                        if counter_description > 2:
                            counter_description = 0
                        await progress_message.edit_text(
                            text=messages.DESCRPIPTION_AND_VIDEO_GENERATION_MESSAGE.format(
                                description_count=list_progress[counter_description],
                                video_count=0,
                            )
                        )
                        counter_description += 1
                    except Exception:
                        pass
                await asyncio.sleep(3)
            else:  # Если по описанию и изображению

                # Проверяем счетчик скачивания на изменение
                if counter != current_step:
                    # Обновляем видео прогресс
                    video_progress = counter / total_step * 100
                    current_step = counter
                    await progress_message.edit_text(
                        text=messages.VIDEO_GENERATION_MESSAGE.format(
                            video_count=video_progress
                        )
                    )
                await asyncio.sleep(1)
        try:
            # Для безопасного ожидания ответа
            msg: ResponseData = await progress_task
        except Exception as e:
            neurobot_video_generation_logger.error_logger.exception(
                format_message(
                    name_router=neurobot_video_generation_logger.router_name,
                    method="<unknown>",
                    error_text=f"Ошибка при генерации видео (vheer): {e}",
                    status=0,
                    url=model_settings.video_gen_models.vheer.VIDEO_URL,
                )
            )
            msg = ResponseData(
                error="Ошибка генерации видео",
                status=0,
                url=model_settings.video_gen_models.vheer.VIDEO_URL,
                method="unknown",
            )

        if msg.message:
            await state.clear()

            # Отправляем пользователю сообщение об успешности запроса
            if description_image:
                await progress_message.edit_text(
                    text=messages.DESCRIPTION_END_AND_VIDEO_GENERATION_END_MESSAGE,
                )
            else:
                await progress_message.edit_text(
                    text=messages.END_VIDEO_GENERATION_MESSAGE
                )
            await asyncio.sleep(1)

            # Отправляем пользователю видео
            await bot.send_video(
                chat_id=message.chat.id,
                video=FSInputFile(path=str(video_path)),
                reply_markup=ReplyKeyboardRemove(),
            )

            await bot.send_message(
                chat_id=message.chat.id,
                text=messages.START_BOT_MESSAGE,
                reply_markup=get_start_button_neuroBot,
            )
        else:
            await state.clear()
            await message.answer(text=f"{msg.error}")

            await bot.send_message(
                chat_id=message.chat.id,
                text=messages.OPTIONS_BOT_MESSAGE,
                reply_markup=get_total_buttons_inline_kb(
                    [
                        InlineKeyboardData(
                            text="1⃣  По Описанию и Изображению",
                            callback_data="vg_vheer description",
                        ),
                        InlineKeyboardData(
                            text="2⃣  По Изображению", callback_data="vg_vheer image"
                        ),
                    ]
                ),
            )

        # Удаляем видео и фото
        if video_path or path_image:
            delete_data(
                list_path=[video_path, path_image],
                warning_logger=neurobot_video_generation_logger.warning_logger,
            )

    else:
        await message.answer(text=messages.NOT_PHOTO_MESSAGE)

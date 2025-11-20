from uuid import uuid4
import asyncio
from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter

from settings.response import messages
from utils.keyboards_utils import get_reply_cancel_button
from erros_handlers.decorator import safe_sync_execution
from neuroBot.utils.selenium import create_selenium_driver
from neuroBot.extensions import (
    bot,
    neurobot_image_generation_logger,
    chrome_selenium_settings,
    get_start_button_neuroBot,
    model_settings,
)
from neuroBot.bot_functions.image_generation import get_an_image_id_by_vheere
from utils.filesistem import delete_data
from erros_handlers.helpers import run_safe_inf_executror
from core.response import ResponseData


router: Router = Router(
    name=model_settings.img_gen_models.vheer.SERVICE_NAME,
)


class VheerImgGenerationFSM(StatesGroup):
    """FSM для генерации изображения для сайта https://vheer.com/."""

    spam: State = State()
    prompt: State = State()


@router.callback_query(
    StateFilter(None),
    F.data == model_settings.img_gen_models.vheer.CALLBACK_BUTTON_DATA,
)
async def img_gen_vheer(call: CallbackQuery, state: FSMContext) -> None:
    """
    Работа с FSM VheerImgGenerationFSM.

    Просит пользователя скинуть описания для изображения.
    """
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer(
        text=messages.IMAGE_DESCRIPTION_MESSAGE,
        reply_markup=get_reply_cancel_button(),
    )

    await state.set_state(VheerImgGenerationFSM.prompt)


@router.message(VheerImgGenerationFSM.prompt, F.text == "Отмена")
async def cancel_vheer_img_gen_handler(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Работа с FSM VheerImgGenerationFSM.

    Отменяет все действия.
    """
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


@router.message(VheerImgGenerationFSM.spam, F.text)
async def get_message_vheer_img_gen_handler(message: Message) -> None:
    """
    Работа с FSM VheerImgGenerationFSM.

    Отправляет пользователю сообщение при наборе им текста во время
    запроса
    """
    await message.reply(
        text=messages.WAIT_MESSAGE,
    )


@router.message(VheerImgGenerationFSM.prompt, F.text)
async def add_prompth_img_gen_vherr(message: Message, state: FSMContext) -> None:
    """
    Работа с FSM VheerImgGenerationFSM.

    Скидывает пользователю сгенерированное изображение
    """
    await state.set_state(VheerImgGenerationFSM.spam)

    await bot.send_message(
        chat_id=message.chat.id,
        text=messages.WAIT_MESSAGE,
        reply_markup=ReplyKeyboardRemove(),
    )

    img_path = None

    decorator_func = safe_sync_execution(
        logging_data=neurobot_image_generation_logger,
    )
    func = decorator_func(create_selenium_driver)

    driver: ResponseData = func(
        driver_path=chrome_selenium_settings.PATH_CHROME_DRIVER,
        add_arument=chrome_selenium_settings.LIST_ADD_ARGUMENT,
        logging_data=neurobot_image_generation_logger,
    )

    if driver.message:
        driver = driver.message

        # Формируем путь до картинки
        img_path: Path = (
            model_settings.img_gen_models.vheer.PATH_TO_IMAGES
            / f"{uuid4().hex}.png"
        )

        loop = asyncio.get_event_loop()

        # для отлова всех возможных ошибок делаем run_safe_inf_executror
        # делаем запрос на генерацию изображения
        img_generate: ResponseData = await run_safe_inf_executror(
            loop,
            get_an_image_id_by_vheere,
            driver,
            model_settings.img_gen_models.vheer.IMAGE_GENERATE,
            message.text,
            img_path,
            neurobot_image_generation_logger,
            logging_data=neurobot_image_generation_logger,
        )

        if img_generate.message:

            await bot.send_message(
                chat_id=message.chat.id,
                text=messages.COMPLETE_GENERATION_MESSAGE,
            )

            await state.clear()
            await bot.send_photo(
                chat_id=message.chat.id, photo=FSInputFile(path=img_path)
            )
            await bot.send_message(
                chat_id=message.chat.id,
                text=messages.START_BOT_MESSAGE,
                reply_markup=get_start_button_neuroBot,
            )

        else:
            await state.set_state(VheerImgGenerationFSM.prompt)
            await message.answer(
                text=f"{img_generate.error}\n{messages.TRY_REPSONSE_MESSAGE}",
                reply_markup=get_reply_cancel_button(),
            )
    else:
        await state.set_state(VheerImgGenerationFSM.prompt)
        await message.answer(
            text=f"{driver.error}\n{messages.TRY_REPSONSE_MESSAGE}",
            reply_markup=get_reply_cancel_button(),
        )

    if img_path:
        delete_data(
            list_path=[img_path],
            warning_logger=neurobot_image_generation_logger.warning_logger,
        )

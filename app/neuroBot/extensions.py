from aiogram import Bot, Dispatcher

from utils.log_utils import setup_bot_logging
from utils.keyboards_utils import (
    get_total_buttons_reply_kb,
    get_total_buttons_inline_kb,
)
from neuroBot.configuration.config import BotSettings
from neuroBot.configuration.image_description import ImaggaImageDescription
from neuroBot.configuration.video_generation import VheerVideoGeneration
from settings.response import settings
from core.config import InlineKeyboardData
from neuroBot.configuration.selenium import SeleniumSettings


# Настройки бота
bot_settings: BotSettings = BotSettings()

# Настройки моделей
img_desc_imagga_settings: ImaggaImageDescription = ImaggaImageDescription()
video_gen_vheer_settings: VheerVideoGeneration = VheerVideoGeneration()

# Создаем бота
bot: Bot = Bot(token=bot_settings.BOT_TOKEN)

# Создаем диспетчер для бота
dp: Dispatcher = Dispatcher()


# Создание кнопок для общих вызовов
get_start_button_neuroBot = get_total_buttons_reply_kb(
    list_text=[
        bot_settings.BOT_ROUTER_REPLY_KB_NAME_1,
        bot_settings.BOT_ROUTER_REPLY_KB_NAME_2,
        bot_settings.BOT_ROUTER_REPLY_KB_NAME_3,
    ],
    quantity_button=1,
)

get_start_buttons_inline_menu_for_image_description = get_total_buttons_inline_kb(
    list_inline_kb_data=[
        InlineKeyboardData(
            text=img_desc_imagga_settings.NAME_ROUTER,
            callback_data=img_desc_imagga_settings.CALLBACK_BUTTON_NAME,
        ),
    ],
    quantity_button=1,
)


get_start_button_inline_menu_for_video_generation = get_total_buttons_inline_kb(
    list_inline_kb_data=[
        InlineKeyboardData(
            text=video_gen_vheer_settings.NAME_ROUTER,
            callback_data=video_gen_vheer_settings.CALLBACK_BUTTON_NAME,
        )
    ],
    quantity_button=1,
)


# Создаем общие логгеры для бота по имени
info_logger, warning_logger, error_logger = setup_bot_logging(
    name=bot_settings.BOT_NAME,
    base_path=bot_settings.ROOT_DIR / "logs",
    log_format=settings.LOG_FORMAT,
    date_format=settings.DATE_FORMAT,
)

# Создаем логгеры для image_description routera
(
    image_description_info_logger,
    image_description_warning_logger,
    image_description_error_logger,
) = setup_bot_logging(
    name=bot_settings.BOT_NAME,
    router_name=bot_settings.BOT_ROUTER_NAME_1,
    base_path=bot_settings.ROOT_DIR / "logs",
    log_format=settings.LOG_FORMAT,
    date_format=settings.DATE_FORMAT,
)
# Создаем логгеры для image_generation routera
(
    image_generation_info_logger,
    image_generation_warning_logger,
    image_generation_error_logger,
) = setup_bot_logging(
    name=bot_settings.BOT_NAME,
    router_name=bot_settings.BOT_ROUTER_NAME_2,
    base_path=bot_settings.ROOT_DIR / "logs",
    log_format=settings.LOG_FORMAT,
    date_format=settings.DATE_FORMAT,
)
# Создаем логгеры для video_generation routera
(
    video_generation_info_logger,
    video_generation_warning_logger,
    video_generation_error_logger,
) = setup_bot_logging(
    name=bot_settings.BOT_NAME,
    router_name=bot_settings.BOT_ROUTER_NAME_3,
    base_path=bot_settings.ROOT_DIR / "logs",
    log_format=settings.LOG_FORMAT,
    date_format=settings.DATE_FORMAT,
)


chrome_selenium_settings: SeleniumSettings = SeleniumSettings()

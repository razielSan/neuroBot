from aiogram import Bot, Dispatcher

from utils.log_utils import setup_bot_logging, init_loggers, get_loggers
from utils.keyboards_utils import (
    get_total_buttons_reply_kb,
    get_total_buttons_inline_kb,
)
from neuroBot.configuration.config import BotSettings


from neuroBot.configuration.selenium import SeleniumSettings
from settings.response import settings
from core.config import InlineKeyboardData
from core.logging import LoggerStorage
from neuroBot.configuration.generation_model.main import BaseGeneration


# Настройки бота
bot_settings: BotSettings = BotSettings()

# Настройки моделей
model_settings = BaseGeneration()


# Создаем бота
bot: Bot = Bot(token=bot_settings.BOT_TOKEN)

# Создаем диспетчер для бота
dp: Dispatcher = Dispatcher()

logging_data: LoggerStorage = LoggerStorage()


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
            text=model_settings.img_desc_models.imagga.CALLBACK_BUTTON_TEXT,
            callback_data=model_settings.img_desc_models.imagga.CALLBACK_BUTTON_DATA,
        ),
    ],
    quantity_button=1,
)


get_start_button_inline_menu_for_video_generation = get_total_buttons_inline_kb(
    list_inline_kb_data=[
        InlineKeyboardData(
            text=model_settings.video_gen_models.vheer.CALLBACK_BUTTON_TEXT,
            callback_data=model_settings.video_gen_models.vheer.CALLBACK_BUTTON_DATA,
        )
    ],
    quantity_button=1,
)


get_start_button_inline_menu_for_image_generation = get_total_buttons_inline_kb(
    list_inline_kb_data=[
        InlineKeyboardData(
            text=model_settings.img_gen_models.pollinations.CALLBACK_BUTTON_TEXT,
            callback_data=model_settings.img_gen_models.pollinations.CALLBACK_BUTTON_DATA,
        ),
        InlineKeyboardData(
            text=model_settings.img_gen_models.caila.CALLBACK_BUTTON_TEXT,
            callback_data=model_settings.img_gen_models.caila.CALLBACK_BUTTON_DATA,
        ),
        InlineKeyboardData(
            text=model_settings.img_gen_models.stablehorde.CALLBACK_BUTTON_TEXT,
            callback_data=model_settings.img_gen_models.stablehorde.CALLBACK_BUTTON_DATA,
        ),
        InlineKeyboardData(
            text=model_settings.img_gen_models.vheer.CALLBACK_BUTTON_TEXT,
            callback_data=model_settings.img_gen_models.vheer.CALLBACK_BUTTON_DATA,
        ),
    ],
    quantity_button=2,
)

# Инициализируем логгеры

init_loggers(
    bot_name=bot_settings.BOT_NAME,
    base_path=bot_settings.ROOT_DIR / "logs",
    log_format=settings.LOG_FORMAT,
    date_format=settings.DATE_FORMAT,
    list_router_name=[
        bot_settings.BOT_ROUTER_NAME_1,
        bot_settings.BOT_ROUTER_NAME_2,
        bot_settings.BOT_ROUTER_NAME_3,
    ],
    setup_bot_logging=setup_bot_logging,
    log_data=logging_data,
)

# Достаем логгеры для каждого отдельного роутера
neurobot_main_logger = get_loggers(
    router_name=bot_settings.BOT_NAME,
    logging_data=logging_data,
)

neurobot_image_description_logger = get_loggers(
    router_name=bot_settings.BOT_ROUTER_NAME_1,
    logging_data=logging_data,
)

neurobot_image_generation_logger = get_loggers(
    router_name=bot_settings.BOT_ROUTER_NAME_2,
    logging_data=logging_data,
)

neurobot_video_generation_logger = get_loggers(
    router_name=bot_settings.BOT_ROUTER_NAME_3,
    logging_data=logging_data,
)


chrome_selenium_settings: SeleniumSettings = SeleniumSettings()

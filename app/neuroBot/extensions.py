from aiogram import Bot, Dispatcher

from utils.log_utils import setup_bot_logging
from neuroBot.configuration.config import BotSettings
from settings.response import settings


# Настройки бота
bot_settings: BotSettings = BotSettings()


# Создаем бота
bot: Bot = Bot(token=bot_settings.BOT_TOKEN)

# Создаем диспетчер для бота
dp: Dispatcher = Dispatcher()


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

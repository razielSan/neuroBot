from core.config import Settings
from core.message import DefaultMessages
from utils.log_utils import setup_bot_logging


settings: Settings = Settings()

messages: DefaultMessages = DefaultMessages()

# Создаем глобальные логгеры для всего приложения
root_info_logger, root_warning_logger, root_error_logger = setup_bot_logging(
    name=settings.BOT_ROOT_NAME,
    base_path=settings.PATH_LOG_FOLDER,
    root_path=True,
    date_format=settings.DATE_FORMAT,
    log_format=settings.LOG_FORMAT,
)

from typing import List
from pathlib import Path

from aiogram.types.bot_command import BotCommand
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """Настройки для бота."""

    # Основные параметры
    BOT_NAME: str = "neuroBot" 
    BOT_ROUTER_NAME_1: str = "image_description"
    BOT_ROUTER_REPLY_KB_NAME_1: str = "Описание Изображений"
    BOT_LOGGING_ERROR_NAME_1: str = f"{BOT_NAME}_{BOT_ROUTER_NAME_1}" # Имя роутера для записи
    # в лог ошибок
    BOT_ROUTER_NAME_2: str = "image_generation"
    BOT_ROUTER_REPLY_KB_NAME_2: str = "Генерация Изображений"
    BOT_LOGGING_ERROR_NAME_2: str = f"{BOT_NAME}_{BOT_ROUTER_NAME_2}"
    BOT_ROUTER_NAME_3: str = "video_generation"
    BOT_ROUTER_REPLY_KB_NAME_3: str = "Генерация видео"
    BOT_LOGGING_ERROR_NAME_3: str = f"{BOT_NAME}_{BOT_ROUTER_NAME_3}"

    # Базовые пути для бота - вычисляются относительно этого файла
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent.parent
    BOT_DIR: Path = ROOT_DIR / BOT_NAME

    # Пути уникальные для бота
    PATH_BOT_STATIC_FOLDER: Path = BOT_DIR / "static"
    PATH_BOT_TEMP_FOLDER: Path = BOT_DIR / "temp"
    PATH_BOT_LOG_FOLDER: Path = ROOT_DIR / "logs" / BOT_NAME

    # Токены и команды
    BOT_TOKEN: str
    LIST_BOT_COMMANDS: List = [
        BotCommand(command="start", description="Главное меню бота")
    ]

    # Конфигурация
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=str(BOT_DIR / ".env"),
        extra="ignore"
    )

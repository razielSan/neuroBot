from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings
from pydantic import BaseModel


class Settings(BaseSettings):
    """Общие настроеки для всего проекта."""

    BOT_ROOT_NAME: str = "root_bot"

    # Базовые пути - вычисляются относительно этого файла
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent  # путь к корневому проекту
    PATH_LOG_FOLDER: Path = ROOT_DIR / "logs"

    # Различные форматы записей
    LOG_FORMAT: str = "[%(asctime)s] - %(module)s:%(lineno)s - [%(levelname)s - %(message)s]"  # формат записи в лог файл
    DATE_FORMAT: str = "%Y-%m-%D %H-%M-%S"  # Формат записи времени


class InlineKeyboardData(BaseModel):
    """Модель для инлайн клавиатуры."""

    text: str
    callback_data: str
    resize_keyboard: Optional[bool] = True

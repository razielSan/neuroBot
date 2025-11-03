from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Общие настроеки для всего проекта."""

    BOT_ROOT_NAME: str = "root_bot"

    # Базовые пути - вычисляются относительно этого файла
    ROOT_DIR: Path = Path(__file__).resolve().parent.parent  # путь к корневому проекту
    PATH_LOG_FOLDER: Path = ROOT_DIR / "logs"

    # Различные форматы записей
    LOG_FORMAT: str = "[%(asctime)s] - %(module)s:%(lineno)s - [%(levelname)s - %(message)s]"  # формат записи в лог файл
    DATE_FORMAT: str = "%Y-%m-%D %H-%M-%S"  # Формат записи времени

from pathlib import Path
from pydantic import BaseModel


class FieldGeneration(BaseModel):
    """Модель содежащая общие настройки для всех моделей."""

    # Основные параметры
    SERVICE_NAME: str = ""  # имя для роутера
    SERVICE_ID: str = ""  # параметр нужный для определеия путей, кнопок

    BOT_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Данные кнопок
    TEXT_PREFIX: str = ""
    CALLBACK_PREFIX: str = ""

    # Данные для папки где будут хранятся изображения
    FOLDER_NAME_IMAGES: str = "" # название папки
    FOLDER_NAME_GENERATION_IMAGES: str = "" # назавние папки моделей

    # Путь до папки с изображениями
    @property
    def PATH_TO_IMAGES(self) -> Path:
        return (
            self.BOT_DIR
            / "temp"
            / self.FOLDER_NAME_IMAGES
            / self.FOLDER_NAME_GENERATION_IMAGES
            / self.SERVICE_ID
        )

    # Текст каллбэк кнопки
    @property
    def CALLBACK_BUTTON_TEXT(self):
        return f"{self.TEXT_PREFIX} {self.SERVICE_ID}"

    # Данные каллбэк кнопки
    @property
    def CALLBACK_BUTTON_DATA(self):
        return f"{self.CALLBACK_PREFIX} {self.SERVICE_ID}"

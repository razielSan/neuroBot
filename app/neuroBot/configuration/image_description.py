from typing import Optional

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class ImaggaImageDescription(BaseSettings):
    """Модель сайта, по описаню изображений, https://imagga.com/."""

    NAME_ROUTER: str = "imagga"
    CALLBACK_BUTTON_NAME: str = "img_desc imagga"
    ID_IMAGGA_AUTHORIZATION: Optional[str]  # Токен аторизации

    # Пути для модели определяются с пути этого файла
    BOT_DIR: Path = Path(__file__).resolve().parent.parent
    PATH_TO_IMAGGA_IMAGES_DESCRIPTION: Path = (
        BOT_DIR / "temp" / "img" / "images_description" / "immaga"
    )

    # URL для доступа к api сайта
    UPLOAD_ENDPOINT: str = "https://api.imagga.com/v2/uploads"  # URL для получения uplooad_image_id картинки
    URL_TAGS: str = "https://api.imagga.com/v2/tags"  # URL для описание изображения

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=BOT_DIR / ".env",
        extra="ignore",
    )

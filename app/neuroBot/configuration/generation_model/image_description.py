from typing import Optional
from pydantic import BaseModel
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from neuroBot.configuration.generation_model.filed import FieldGeneration


class Imagga(FieldGeneration, BaseSettings):
    """Модель для сайта https://imagga.com/."""

    SERVICE_NAME: str = "ImgDesc Imagga"
    SERVICE_ID: str = "imagga"

    TEXT_PREFIX: str = "1⃣"
    CALLBACK_PREFIX: str = "img_desc"

    FOLDER_NAME_IMAGES: str = "img"
    FOLDER_NAME_GENERATION_IMAGES: str = "images_description"

    ID_IMAGGA_AUTHORIZATION: Optional[str] = None

    # URL для доступа к api сайта
    UPLOAD_ENDPOINT: str = "https://api.imagga.com/v2/uploads"  # URL для получения uplooad_image_id картинки
    URL_TAGS: str = "https://api.imagga.com/v2/tags"  # URL для описание изображения

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        extra="ignore",
        env_prefix="imagga__",
    )


class ImgDescGenerationModels(BaseModel):
    """Модель собирающая модели для описания изображений."""

    imagga: Imagga = Imagga()

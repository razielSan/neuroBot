from typing import Optional
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class PollinationsImageGeneration(BaseModel):
    """Модель сайта https://pollinations.ai/."""

    # Основные параметры
    NAME_ROUTER: str = "Pollinations"
    CALLBACK_BUTTON_TEXT: str = "1⃣ Pollinations"
    CALLBACK_BUTTON_DATA: str = "img_gen Pollinations"

    IMAGE_GENERATE: str = (
        "https://image.pollinations.ai/prompt/{text}"  # URL для генерации изображений
    )

    # Пути для модели определяются с пути этого файла
    BOT_DIR: Path = Path(__file__).resolve().parent.parent
    PATH_TO_POLLINATIONS_IMAGES_GENERATION: Path = (
        BOT_DIR / "temp" / "img" / "images_generation" / "pollinations"
    )


class CailaIoImageGeneration(BaseSettings):
    """Модель сайта https://caila.io/."""

    # Основные параметры
    NAME_ROUTER: str = "Caila"
    CALLBACK_BUTTON_TEXT: str = "2⃣ Caila"
    CALLBACK_BUTTON_DATA: str = "img_gen Caila"
    APIKEY_CAILA_IG: Optional[str] = None
    URL_IMAGE_GENERATE: str = "https://caila.io/api/adapters/openai/images/generations"

    # Модели для генерации
    MODEL_GPT_IMAGE_1_NAME: str = "gpt-image-1"  # имя модели
    MODEL_GPT_IMAGE_1_TEXT: str = "1⃣ gpt-image-1"  # имя на callback кнопке
    MODEL_GPT_IMAGE_1_DATA: str = "img_gen caila gpt-image-1"  # callback data
    MODEL_DALI_E_3_NAME: str = "dall-e-3"
    MODEL_DALI_E_3_TEXT: str = "2⃣ dall-e-3"
    MODEL_DALI_E_3_DATA: str = "img_gen caila dall-e-3"

    # Пути для модели определяются с пути этого файла
    BOT_DIR: Path = Path(__file__).resolve().parent.parent
    PATH_TO_CAILA_IMAGES_GENERATION: Path = (
        BOT_DIR / "temp" / "img" / "images_generation" / "caila"
    )

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=BOT_DIR / ".env",
        extra="ignore",
    )

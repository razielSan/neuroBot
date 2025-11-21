from typing import Optional
from pathlib import Path

from pydantic import BaseModel
from neuroBot.configuration.generation_model.filed import FieldGeneration


class Pollinations(FieldGeneration, BaseModel):
    """Модель сайта https://pollinations.ai/."""

    SERVICE_ID: str = "ImgGen Pollinations"
    SERVICE_ID: str = "pollinations"

    FOLDER_NAME_IMAGES: str = "img"
    FOLDER_NAME_GENERATION_IMAGES: str = "images_generation"

    TEXT_PREFIX: str = "1⃣"
    CALLBACK_PREFIX: str = "img_gen"

    IMAGE_GENERATE: str = (
        "https://image.pollinations.ai/prompt/{text}"  # URL для генерации изображений
    )


class Caila(FieldGeneration, BaseModel):
    """Модель сайта https://caila.io/."""

    # Основные параметры

    SERVICE_NAME: str = "ImgGen Caila"
    SERVICE_ID: str = "caila"

    FOLDER_NAME_IMAGES: str = "img"
    FOLDER_NAME_GENERATION_IMAGES: str = "images_generation"

    TEXT_PREFIX: str = "2⃣"
    CALLBACK_PREFIX: str = "img_gen"

    APIKEY_CAILA_IG: Optional[str] = None

    # URL для запроса
    URL_IMAGE_GENERATE: str = "https://caila.io/api/adapters/openai/images/generations"

    # Модели для генерации
    MODEL_GPT_IMAGE_1_NAME: str = "gpt-image-1"  # имя модели
    MODEL_GPT_IMAGE_1_TEXT: str = "1⃣ gpt-image-1"  # имя на callback кнопке
    MODEL_GPT_IMAGE_1_DATA: str = "img_gen caila gpt-image-1"  # callback data
    MODEL_DALI_E_3_NAME: str = "dall-e-3"
    MODEL_DALI_E_3_TEXT: str = "2⃣ dall-e-3"
    MODEL_DALI_E_3_DATA: str = "img_gen caila dall-e-3"


class Stablehorde(FieldGeneration, BaseModel):
    """Модель сайта https://stablehorde.net."""

    # Основыне параметры
    SERVICE_NAME: str = "ImgGen Stablehorde"
    SERVICE_ID: str = "stablehorde"

    FOLDER_NAME_IMAGES: str = "img"
    FOLDER_NAME_GENERATION_IMAGES: str = "images_generation"

    TEXT_PREFIX: str = "3⃣"
    CALLBACK_PREFIX: str = "img_gen"

    APIKEY_STABLEHORDE_IG: Optional[str] = None

    # URL для запроса
    REQUESTS_TO_GENERATE_IMAGES: str = "https://stablehorde.net/api/v2/generate/async"  # запроса на генерации изображений
    REQUESTS_STATUS_CHECK_WITHOUT_IMAGES: str = (
        "https://stablehorde.net/api/v2/generate/check/{id}"
    )
    REQUESTS_FULL_STATUS_IMAGE_GENERATIONS: str = (
        "https://stablehorde.net/api/v2/generate/status/{id}"
    )


class Vheer(FieldGeneration, BaseModel):
    """Модель сайта https://vheer.com/."""

    # Основные параметры
    SERVICE_NAME: str = "ImgGen Vheer"
    SERVICE_ID: str = "vheer"

    FOLDER_NAME_IMAGES: str = "img"
    FOLDER_NAME_GENERATION_IMAGES: str = "images_generation"

    TEXT_PREFIX: str = "4⃣"
    CALLBACK_PREFIX: str = "img_gen"

    IMAGE_GENERATE: str = (
        "https://vheer.com/app/text-to-image"  # URL для генерации изображений
    )


class ImgGenerationModels(BaseModel):
    """Модель собирающая модели для генерации изображений."""

    pollinations: Pollinations = Pollinations()
    caila: Caila = Caila()
    vheer: Vheer = Vheer()
    stablehorde: Stablehorde = Stablehorde()

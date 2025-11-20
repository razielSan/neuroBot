from typing import List

from pydantic import BaseModel
from pathlib import Path
from neuroBot.configuration.generation_model.filed import FieldGeneration


class Vheer(FieldGeneration, BaseModel):
    """Модель для сайта https://vheer.com."""

    TOTAL_STEP: int = (
        10  # Общее количество шагов для отслеживания прогресс загрузки видео
    )

    SERVICE_NAME: str = "VideoGen Vheer"
    SERVICE_ID: str = "vheer"

    TEXT_PREFIX: str = "1⃣ "
    CALLBACK_PREFIX: str = "video_gen"

    FOLDER_NAME_IMAGES: str = "img"
    FOLDER_NAME_GENERATION_IMAGES: str = "images_generation"

    PATH_TO_VIDEO: Path = (
        Path(__file__).resolve().parent.parent.parent
        / "temp"
        / "video"
        / "video_generation"
        / SERVICE_ID
    )

    VIDEO_URL: str = "https://vheer.com/app/image-to-video"  # URL генерации видео

    # URL сайтов по описании изображений

    PROMPT_IMG_URL_BY_PRODUCTS_APSOSE: str = (
        "https://products.aspose.ai/pdf/ru/image-description"
    )
    PROMPT_IMG_URL_BY_DESCRIBEPICTURE_CC: str = "https://describepicture.cc/ru"

    DEFAULT_LIST_DESCRIPTION_IMAGES: List[str] = [
        "the image is moving",
        "the image moves forward",
        "the image moves backwards",
        "the image moves to the left",
        "the image moves to the right",
    ]  # Дефолтные сообщение для описания изображения

    VIDEO_DATA: str = """
        const video = arguments[0];
        const done = arguments[1];
        fetch(video.src)
            .then(r => r.blob())
            .then(blob => {
            const reader = new FileReader();
            reader.onload = () => done(reader.result);
            reader.readAsDataURL(blob);
            })
            .catch(err => done('ERROR:' + err.message));
        """  # JavaScripts для загрузки видео


class VideoGenerationModels(BaseModel):
    """Модель собирающая модели для генерации видео."""

    vheer: Vheer = Vheer()

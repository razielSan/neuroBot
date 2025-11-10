from pathlib import Path
from typing import List

from pydantic import BaseModel


class VheerVideoGeneration(BaseModel):
    """Модель генерации изображений для сайта https://vheer.com/."""

    TOTAL_STEP: int = (
        10  # Общее количество шагов для отслеживания прогресс загрузки видео
    )
    NAME_ROUTER: str = "1⃣  vheer"
    CALLBACK_BUTTON_NAME: str = "video_gen vheer"  # callback запись в инлайн клавиатуре
    VIDEO_URL: str = "https://vheer.com/app/image-to-video"

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

    PATH_TO_IMAGE_VHEER: Path = (
        Path(__file__).resolve().parent.parent
        / "temp"
        / "img"
        / "video_generation"
        / "vheer"
    )  # Временные путь для хранения фото скидываемый пользователем

    PATH_TO_VIDEO_VHEER: Path = (
        Path(__file__).resolve().parent.parent
        / "temp"
        / "video"
        / "video_generation"
        / "vheer"
    )  # Временный путь для сгенерированного видео

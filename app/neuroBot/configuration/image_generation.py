from pathlib import Path

from pydantic import BaseModel


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
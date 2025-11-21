from pathlib import Path

from neuroBot.configuration.generation_model.video_generation import (
    VideoGenerationModels,
)
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from neuroBot.configuration.generation_model.image_description import (
    ImgDescGenerationModels,
)
from neuroBot.configuration.generation_model.image_generation import ImgGenerationModels


class BaseGeneration(BaseSettings):
    """Общий класс для генерации моделей."""

    video_gen_models: VideoGenerationModels = VideoGenerationModels()
    img_desc_models: ImgDescGenerationModels = ImgDescGenerationModels()
    img_gen_models: ImgGenerationModels = ImgGenerationModels()

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        extra="ignore",
        env_nested_delimiter="__",
    )

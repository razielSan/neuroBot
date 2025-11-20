from neuroBot.configuration.generation_model.video_generation import (
    VideoGenerationModels,
)
from pydantic import BaseModel
from neuroBot.configuration.generation_model.image_description import (
    ImgDescGenerationModels,
)
from neuroBot.configuration.generation_model.image_generation import ImgGenerationModels


class BaseGeneration(BaseModel):
    """Общий класс для генерации моделей."""

    video_gen_models: VideoGenerationModels = VideoGenerationModels()
    img_desc_models: ImgDescGenerationModels = ImgDescGenerationModels()
    img_gen_models: ImgGenerationModels = ImgGenerationModels()

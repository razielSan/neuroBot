from typing import Optional, Any

from pydantic import BaseModel


class ResponseData(BaseModel):
    """Модель для возвращения ответов."""

    error: Optional[str] = None
    message: Optional[Any] = None
    status: Optional[int] = None
    url: Optional[str] = None
    method: Optional[str] = None


class InlineKeyboardData(BaseModel):
    """Модель для инлайн клавиатуры."""
    text: str
    callback_data: str
    resize_keyboard: Optional[bool] = True

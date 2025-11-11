from typing import Optional, Any
from logging import Logger
from dataclasses import dataclass

from pydantic import BaseModel


class ResponseData(BaseModel):
    """Модель для возвращения ответов."""

    error: Optional[str] = None
    message: Optional[Any] = None
    status: Optional[int] = None
    url: Optional[str] = None
    method: Optional[str] = None


@dataclass
class LoggingData:
    "Модель для возврата логгеров."
    info_logger: Logger
    warning_logger: Logger
    error_logger: Logger
    router_name: str

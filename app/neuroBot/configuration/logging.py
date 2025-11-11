from typing import Dict
from dataclasses import dataclass

from pydantic import BaseModel


class LoggerSettings(BaseModel):
    BOT_ROUTER_NAME: Dict = {}

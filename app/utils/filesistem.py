from typing import Tuple
from pathlib import Path


def ensure_derictories(*args: Path) -> None:
    """
    Проверяет наличие переданных путей и создает их при необходимости

    """
    requiered_dirs: Tuple[Path, ...] = args

    for dir in requiered_dirs:
        dir.mkdir(parents=True, exist_ok=True)

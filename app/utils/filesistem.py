from typing import Tuple, Optional
from pathlib import Path
from logging import Logger


def ensure_derictories(*args: Path) -> None:
    """
    Проверяет наличие переданных путей и создает их при необходимости

    """
    requiered_dirs: Tuple[Path, ...] = args

    for dir in requiered_dirs:
        dir.mkdir(parents=True, exist_ok=True)


def delete_data(
    path: Path,
    warning_logger: Optional[Logger] = None,
) -> None:
    """Удаляет данные по переданному пути

    Args:
        path (Path): Путь до данных
        warning_logger (Optional[Logger], optional): логгер для записи в лог(По умолчанию None)
    """
    try:
        if path.exists():
            path.unlink()
    except Exception as err:
        message: str = f"Ошибка при удалении {path}: {err}"
        if warning_logger:
            warning_logger.exception(msg=message)

from typing import Optional, Tuple
from pathlib import Path
from logging import (
    Formatter,
    StreamHandler,
    FileHandler,
    getLogger,
    Logger,
    ERROR,
    INFO,
    WARNING,
)
from sys import stdout


def setup_bot_logging(
    name: str,
    base_path: Path,
    log_format: str,
    date_format: str,
    root_path: Optional[Path] = False,
    router_name: Optional[str] = None,
) -> Tuple[Logger, Logger, Logger]:
    """
    Создаем логгеры для бота: Обычный, предупреждающий и для ошибок
    Логи будут лежать в logs/<bot_name>/<тип логгирования>.log

    Args:
        name (str): Имя бота
        base_path (Path): Путь до папки с логами
        router_name (str, optional): Имя папки для конкретного роутера, если нужно,
        если нет будет сохранятся в base_path
        root_path (str, Optional):  По умолчанию(False) логгирует в папку по имени бота(
            True - логирует в глобальный лог
        )
    """

    # Формируем имя логгеров для того чтобы все не записывались в один
    logger_name: str = name if not router_name else f"{name}_{router_name}"

    # Если root_path передан, пропускам - логируем в глобальный лог
    # Если root_path по умолчанию(Fals) - логируем в папку по имени бота
    if not root_path:
        base_path: Path = base_path / name  # Путь до папки с логами

    # Если перадано имя конкретного роутера
    if router_name:
        base_path = base_path / router_name

    info_path: Path = base_path / "info.log"
    warning_path: Path = base_path / "warning.log"
    error_path: Path = base_path / "error.log"

    # Создаем папку "logs" если ее нет
    base_path.mkdir(parents=True, exist_ok=True)

    # Потоковый обработчик для вывода в
    formaterr: Formatter = Formatter(
        fmt=log_format,
        datefmt=date_format,
    )

    # Потоковый обработчик для вывода в консоль
    stream_handler: StreamHandler = StreamHandler(stream=stdout)
    stream_handler.setFormatter(formaterr)

    # Файловые обработчики
    file_handler_info: FileHandler = FileHandler(
        filename=info_path,
        encoding="utf-8",
    )
    file_handler_info.setFormatter(formaterr)

    file_handler_warning: FileHandler = FileHandler(
        filename=warning_path, encoding="utf-8"
    )
    file_handler_warning.setFormatter(formaterr)

    file_handler_error: FileHandler = FileHandler(
        filename=error_path,
        encoding="utf-8",
    )
    file_handler_error.setFormatter(formaterr)

    # Логгер для информации
    info_logger: Logger = getLogger(f"{logger_name}_info")
    if not info_logger.handlers:
        info_logger.setLevel(level=INFO)
        info_logger.addHandler(file_handler_info)
        info_logger.addHandler(stream_handler)

    # Логгер для предупреждения
    warning_logger: Logger = getLogger(f"{logger_name}_warning")
    if not warning_logger.handlers:
        warning_logger.setLevel(level=WARNING)
        warning_logger.addHandler(file_handler_warning)
        warning_logger.addHandler(stream_handler)

    # Логгер для ошибок
    error_logger: Logger = getLogger(f"{logger_name}_error")
    if not error_logger.handlers:
        error_logger.setLevel(level=ERROR)
        error_logger.addHandler(file_handler_error)
        error_logger.addHandler(stream_handler)

    return info_logger, warning_logger, error_logger

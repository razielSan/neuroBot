from typing import List
from core.response import ResponseData
from settings.response import messages
from logging import Logger

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from erros_handlers.format import format_message
from core.response import LoggingData


def create_selenium_driver(
    # name_router: str,
    driver_path: str,
    add_arument: List[str],
    logging_data: LoggingData,
    automatisation: bool = True,
    browser: str = "chrome",
) -> ResponseData:
    """Создаем driver для selenium

    Args:
        driver_path (str): Путь до папки с драйвером
        add_arument (List[str]): Список аргументов для драйвера
        logging_data (LoggingData): Класс содержащий логгер и имя роутера для записи в лог
        automatisation (bool, optional): Отключаем флаги автоматизации(True/False)
        True - по умолчанию
        browser (str, optional): Имя браузера("chrome")
        chrome - по умолчанию

    Returns:
        ResponseData: Объект с результатом запроса.

        Атрибуты ResponseData:
            - message (Any | None): Данные успешного ответа (если запрос прошёл успешно).
            - error (str | None): Описание ошибки, если запрос завершился неудачей.
            - status (int): HTTP-код ответа. 0 — если ошибка возникла на клиентской стороне.
            - url (str): URL, по которому выполнялся запрос.
            - method (str): HTTP-метод, использованный при запросе.
    """

    try:
        if browser == "chrome":
            service: Service = Service(executable_path=driver_path)
            options: Options = Options()

            # Добавляем опции
            for data in add_arument:
                options.add_argument(data)
            if automatisation:  # Отлючаем флаги автоматизации
                options.add_experimental_option(
                    "excludeSwitches", ["enable-automation"]
                )
                options.add_experimental_option("useAutomationExtension", False)
            driver = webdriver.Chrome(options=options, service=service)
            return ResponseData(
                message=driver, status=0, method="<unkown>", url="<unknown>"
            )
    except Exception as err:
        logging_data.error_logger.exception(
            msg=format_message(
                name_router=logging_data.router_name,
                method="<unknown>",
                status=0,
                url="<unknown>",
                error_text=f"Произошла обшибка при создании драйвера - {err}",
            )
        )

        return ResponseData(
            error=messages.SERVER_ERROR,
            url="<unknown>",
            method="<unknown>",
            status=0,
        )

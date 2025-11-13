from typing import List, Optional
from pathlib import Path
import aiohttp
from logging import Logger
from erros_handlers.format import format_message
from settings.response import messages

from erros_handlers.main import error_handler_for_the_website


from core.response import ResponseData, LoggingData


async def get_image_description_by_immaga(
    key_autorization: str,
    upload_endpoint: str,
    url_tags: str,
    path_img: Path,
    session: aiohttp.ClientSession,
    logging_data: LoggingData,
    language="en",
    limit=-1,
) -> ResponseData:
    """Получает описание картинки для сайта https://imagga.com/.

    Args:
        key_autorization (str): Токен аторизации
        upload_endpoint (str): URL для получения uplooad_image_id картинки
        url_tags (str): URL для описание изображения
        path_img (Path): Путь до картинки для описания изображений
        logging_data (LoggingData): Класс содержащий в себе логгер и имя роутера для записи в лог
        name_router (str, Optional): Имя роутера для записи в лог файл при ошибке(По умолчанию Nonr)
        language (str, optional): Язык описания изображений.По умолчанию английский
        limit (int, optional): Количество описаний.По умолчанию максимальное

    Returns:
        ResponseData: Объект с результатом запроса.

        Атрибуты ResponseData:
            - message (Any | None): Данные успешного ответа (если запрос прошёл успешно).
            - error (str | None): Описание ошибки, если запрос завершился неудачей.
            - status (int): HTTP-код ответа. 0 — если ошибка возникла на клиентской стороне.
            - url (str): URL, по которому выполнялся запрос.
            - method (str): HTTP-метод, использованный при запросе.
    """
    # Отправляем картинку на сайт для ее описания
    with open(path_img, "rb") as file:
        response: ResponseData = await error_handler_for_the_website(
            session=session,
            url=upload_endpoint,
            headers={
                "Authorization": f"Basic {key_autorization}",
            },
            data={"image": file},
            method="POST",
            logging_data=logging_data,
            function_name=get_image_description_by_immaga.__name__,
        )

    if response.error:
        return response

    # Получаем upload_id картинки
    upload_id: str = response.message["result"]["upload_id"]

    # Делаем запрос на получение описание изображения
    response_image_description: ResponseData = await error_handler_for_the_website(
        session=session,
        url=f"{url_tags}?image_upload_id="
        f"{upload_id}&language={language}&limit={limit}",
        headers={
            "Authorization": f"Basic {key_autorization}",
        },
        logging_data=logging_data,
        function_name=get_image_description_by_immaga.__name__,
    )
    if response_image_description.error:
        return response_image_description

    # Формируем данные для описания картинки
    array_image_description: List = [
        "Список возможных вариантов изображения на картинке:\n\n"
    ]

    for data in response_image_description.message["result"]["tags"]:
        array_image_description.append(
            f"{data['tag'][language].title()} ({data['confidence']:.3f}%) "
        )

    mess: str = "\n".join(array_image_description)
    return ResponseData(
        message=mess,
        status=200,
        method=response_image_description.method,
        url=response_image_description.url,
    )

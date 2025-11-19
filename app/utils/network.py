from aiohttp import ClientSession
from typing import Optional
import base64
from pathlib import Path
from core.response import LoggingData

from selenium.webdriver.remote.webelement import WebElement

from erros_handlers.main import error_handler_for_the_website
from erros_handlers.format import format_message
from core.response import LoggingData, ResponseData
from settings.response import messages


async def get_and_save_image(
    data_requests: str,
    path_img: str,
    session: ClientSession,
    logging_data: LoggingData,
    base_64: Optional[bool] = None,
) -> ResponseData:
    """
    Сохраняет data_requests по указанному если base_64 = True.

    Если data_requests это URL.Заходит по url, скачивает изображение
    и сохраняет его по указанному пути

    Args:
        data_requests (str): url для скачивания или строка в кодировке base64
        path_img (str): Путь до картинки
        session (ClientSession): сессия для запроса
        logging_data (LoggingData): обьект класса LoggingData содержащий в себе логгер и имя роутера
        base_64 (Optional[bool], optional): Проверка на кодировку base_64. По умолачанию None

    Returns:
        ResponseData: Объект с результатом запроса.

        Атрибуты ResponseData:
            - message (Any | None): Данные успешного ответа (если запрос прошёл успешно).
            - error (str | None): Описание ошибки, если запрос завершился неудачей.
            - status (int): HTTP-код ответа. 0 — если ошибка возникла на клиентской стороне.
            - url (str): URL, по которому выполнялся запрос.
            - method (str): HTTP-метод, использованный при запросе.
    """
    if base_64:
        image_file = base64.b64decode(data_requests)
        with open(path_img, "wb") as image:
            image.write(image_file)
    else:
        # Делаем запрос на сайт для получения данных о картинке
        response: ResponseData = await error_handler_for_the_website(
            session=session,
            url=data_requests,
            logging_data=logging_data,
            data_type="BYTES",
            timeout=180,
            function_name=get_and_save_image.__name__,
        )

        if response.error:
            return response

        # Сохраняем картинку по переданному пути
        with open(path_img, "wb") as file:
            file.write(response.message)

    return ResponseData(
        message=path_img,
        url="<unknown>",
        method="GET",
        status=200,
    )


def save_blob_image(
    driver,
    img_element: WebElement,
    img_path: Path,
    logging_data: LoggingData,
):
    """
    Сохраняет blob изображение из элемента.
    """
    try:
        # Получаем base64 через Canvas
        base64_data = driver.execute_script(
            """
        var img = arguments[0];
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        ctx.drawImage(img, 0, 0);
        return canvas.toDataURL('image/png');
        """,
            img_element,
        )

        # Декодируем и сохраняем
        base64_image = base64_data.split(",")[1]
        image_data = base64.b64decode(base64_image)

        with open(img_path, "wb") as f:
            f.write(image_data)

        return ResponseData(
            message=img_path,
            url="<unknown>",
            method="<unknown>",
            status=200,
        )

    except Exception as err:
        if logging_data:
            logging_data.error_logger.exception(
                format_message(
                    name_router=logging_data.router_name,
                    status=0,
                    method="<unknown>",
                    url="<unknown>",
                    error_text=f"Ошибка при сохранении изображения - {err}",
                    function_name=save_blob_image.__name__,
                )
            )
        return ResponseData(
            error=messages.SERVER_ERROR,
            url="<unknwon>",
            method="<unknown>",
            status=0,
        )

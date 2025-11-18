import json
from typing import Dict, Optional, Callable
import asyncio
from time import time

from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext

from erros_handlers.main import error_handler_for_the_website
from core.response import LoggingData, ResponseData


async def get_url_video_generate_by_caila(
    url: str,
    api_key: str,
    model: str,
    promtp: str,
    session: ClientSession,
    logging_data: LoggingData,
    size: str = "1024x1024",
    quality_gpt_image_1: str = "low",
    quality_dall_e_3: str = "standard",
    timeout: int = 300,
) -> ResponseData:
    """
    Работа с сайтом https://caila.io/.

    Возвращает b64_json или url для скачивания изображения.

    Args:
        url (str): URL генерации изображения
        api_key (str): API Key для доступа
        model (str): модель генерации изображения
        promtp (str): описание изображения
        session: (ClientSession): сессия для запроса
        logging_data: (LoggingData): обьект класса LoggingData содержащий логгер и имя роутера
        size (str, optional): размер изображения
        quality_gpt_image_1 (str, optional): качество для модели gpt-image-1
        quality_dall_e_3 (str, optional): качество для модели dall-e-3
        timeout (int, Optional): время в секундах на ожидание запроса

    Returns:
        ResponseData: Объект с результатом запроса.

        Атрибуты ResponseData:
            - message (Any | None): Данные успешного ответа (если запрос прошёл успешно).
            - error (str | None): Описание ошибки, если запрос завершился неудачей.
            - status (int): HTTP-код ответа. 0 — если ошибка возникла на клиентской стороне.
            - url (str): URL, по которому выполнялся запрос.
            - method (str): HTTP-метод, использованный при запросе.
    """
    quality: str = "low"
    if model == "gpt-image-1":
        quality = quality_gpt_image_1
    elif model == "dall-e-3":
        quality = quality_dall_e_3

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    json_data = json.dumps(
        {
            "model": f"just-ai/openai-proxy/{model}",
            "prompt": promtp,
            "quality": quality,
            "size": size,
        }
    )
    response_img: ResponseData = await error_handler_for_the_website(
        session=session,
        url=url,
        logging_data=logging_data,
        headers=HEADERS,
        data=json_data,
        method="POST",
        timeout=timeout,
    )
    if response_img.error:
        return response_img

    if model == "dall-e-3":
        message = response_img.message["data"][0]["url"]
    elif model == "gpt-image-1":
        message = response_img.message["data"][0]["b64_json"]

    return ResponseData(
        url=url,
        method="POST",
        status=200,
        message=message,
    )


async def get_an_image_id_by_stablehorde(
    url: str,
    api_key: str,
    prompt: str,
    session: ClientSession,
    logging_data: LoggingData,
    width: int = 512,
    height: int = 512,
    timeout: int = 60,
) -> ResponseData:
    """
    Работа с сайтом https://stablehorde.net.

    Возвращает обьект класс ResponseData содержащий id картинки

    Args:
        url (str): url для запроса на генерацию изображения
        api_key (str): api ключ для генерации
        prompt (str): описание изображения
        session (ClientSession): сессия для запроса
        logging_data (LoggingData): Обьект класса LoggingData содержащий логгер и имя роутера
        width (int, optional): Ширина картинки. По умолчанию 512.
        height (int, optional): Высота картинки. По умолчанию 512.
        timeout (int, optional): время в секундах на ожидание запроса

    Returns:
        ResponseData: Объект с результатом запроса.

        Атрибуты ResponseData:
            - message (Any | None): Данные успешного ответа (если запрос прошёл успешно).
            - error (str | None): Описание ошибки, если запрос завершился неудачей.
            - status (int): HTTP-код ответа. 0 — если ошибка возникла на клиентской стороне.
            - url (str): URL, по которому выполнялся запрос.
            - method (str): HTTP-метод, использованный при запросе.
    """
    payload: Dict = {
        "prompt": prompt,
        "params": {
            "sampler_name": "k_euler_a",
            "steps": 30,
            "cfg_scale": 7,
            "width": width,
            "height": height,
        },
        "nsfw": False,
        "censor_nsfw": True,
    }

    headers: Dict = {"apikey": api_key, "Client-Agent": "MyApp:1.0:github.com/me"}

    respons_img_id: ResponseData = await error_handler_for_the_website(
        session=session,
        url=url,
        headers=headers,
        json=payload,
        logging_data=logging_data,
        function_name=get_an_image_id_by_stablehorde.__name__,
        method="POST",
        timeout=timeout,
    )

    warning = None
    # Проверяем на наличие worker
    if respons_img_id.message:
        warning: Optional[str] = (
            "Ни один доступный сотрудник не может выполнить этот запрос"
            if respons_img_id.message.get("message")
            else warning
        )
    if respons_img_id.error or warning:
        # если нету доступных сотрудников
        if warning:
            respons_img_id.message = None
            respons_img_id.error = warning
        return respons_img_id
    return respons_img_id


async def check_status_without_images_by_stablehorde(
    api_key: str,
    url: str,
    job_id: int,
    session: ClientSession,
    logging_data: LoggingData,
    time_working: int = 20,
    full_status_url: bool = False,
    update_progress: Callable = None,
    timeout: int = 120,
) -> ResponseData:
    """
    Работа с сайтом https://stablehorde.net.

    full_status_url = False - Проверяет сайт на наличие доступности изображения
    в цикле в течении time_working
    full_status_url = True - Получает полный результат сайта с сгенерированной картинкой
    если есть

    Args:
        api_key (str): api ключ для сайта
        url (str): url для проверки
        job_id (int): id картинки
        session (ClientSession): сессия для запроса
        logging_data (LoggingData): Обьект класса LoggingData содержащий логгер и имя роутера
        time_working (int): время в минутах на ожидание
        full_status_url (bool, optional): флаг для указания запроса на полный результат
        сайта с сгенерированной картинкой.По умолчанию False
        update_progress (Callable, optional): Функция для отслеживания прогресса. По умолчанию None.
        timeout (int, optional): время в секундах на ожидание запроса

    Returns:
        ResponseData: Объект с результатом запроса.

        Атрибуты ResponseData:
            - message (Any | None): Данные успешного ответа (если запрос прошёл успешно).
            - error (str | None): Описание ошибки, если запрос завершился неудачей.
            - status (int): HTTP-код ответа. 0 — если ошибка возникла на клиентской стороне.
            - url (str): URL, по которому выполнялся запрос.
            - method (str): HTTP-метод, использованный при запросе.
    """
    # Формируем url
    url: str = url.format(id=job_id)

    headers: Dict = {"apikey": api_key, "Client-Agent": "MyApp:1.0:github.com/me"}

    # Делаем запрос на получение информации с сайта
    respons_status: ResponseData = await error_handler_for_the_website(
        session=session,
        url=url,
        headers=headers,
        logging_data=logging_data,
        function_name=get_an_image_id_by_stablehorde.__name__,
        timeout=timeout,
    )
    if respons_status.error:
        return respons_status

    # если был указан запрос на получение полной информации то возвращаем его
    if full_status_url:
        return respons_status

    wait_time = respons_status.message.get("wait_time")

    # Создаем текущее и конечное время
    current_time: float = time()
    result_time: int = current_time + (time_working * 60)
    # Встаем в цикл
    while current_time > 0:
        current_time = result_time - time()
        # делаем запрос на получение времени оставшегося до завершения создания изображения
        respons_status: ResponseData = await error_handler_for_the_website(
            session=session,
            url=url,
            headers=headers,
            logging_data=logging_data,
            function_name=get_an_image_id_by_stablehorde.__name__,
            timeout=timeout,
        )
        if respons_status.error:
            return respons_status

        wait_time: int = respons_status.message.get("wait_time")
        finished: int = respons_status.message.get("finished", 0)

        # Если картинка готова то выходим
        if finished > 0:
            break

        # На случай непредвиденных ситуаций
        try:
            data = await update_progress(data_state=wait_time)
            if not data:
                break

        except Exception:
            pass

        await asyncio.sleep(20)

    # Проверяем на истечение времени
    if current_time <= 0:
        respons_status.message = None
        respons_status.error = "Время ожидания истекло"
    return respons_status

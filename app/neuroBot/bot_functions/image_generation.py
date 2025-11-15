import json

from aiohttp import ClientSession
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
        timeout=180,
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

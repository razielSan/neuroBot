from typing import Dict
from logging import Logger
import asyncio

import aiohttp

from core.response import ResponseData


async def safe_read_response(resp):
    """Проверяет в каком формате был передан ответ с сайта и возвращает текст ответа

    Args:
        resp (_type_): запрос для сайта

    Returns:
        _type_: Возвращает содержание текста ответа с сайта
    """
    try:
        content_type = resp.headers.get("Content-Type", "").lower()
        if "application/json" in content_type:
            data = await resp.json()
            return data
        return await resp.text()
    except Exception:
        return "<no body>"


async def error_handler_for_the_website(
    session: aiohttp.ClientSession,
    url: str,
    error_logging: Logger,
    name_router: str,
    data_type="JSON",
    timeout=20,
    method="GET",
    data=None,
    headers=None,
) -> ResponseData:
    """

    Асинхронный запрос с обработками ошибок для сайтов

    Args:
        session (_type_): асинхронная сессия запроса
        url (str): URL сайта
        error_logging: (Logger): Логгер для записи ошибки в лог файл
        name_router: (str): Имя роутера в котором произошла ошибка
        data_type (str, optional): Тип возвращаемых данных.По умолчанию JSON('JSON', 'TEXT', 'BYTES')
        timeout (int, optional): таймаут запроса в секундах
        method (str, optional): Метод запроса. 'POST' или "GET"
        data (_type_, optional): Данные для POST запроса
        headers (dict): Заголовки запроса

    Returns:
        ResponseData: Объект с результатом запроса.

        Атрибуты ResponseData:
            - message (Any | None): Данные успешного ответа (если запрос прошёл успешно).
            - error (str | None): Описание ошибки, если запрос завершился неудачей.
            - status (int): HTTP-код ответа. 0 — если ошибка возникла на клиентской стороне.
            - url (str): URL, по которому выполнялся запрос.
            - method (str): HTTP-метод, использованный при запросе.
    """
    # Чтобы не ждать бесконечно при connect/read
    timeout_cfg: aiohttp.ClientTimeout = aiohttp.ClientTimeout(total=timeout)
    try:
        async with session.request(
            method,
            url,
            timeout=timeout_cfg,
            data=data,
            headers=headers,
        ) as resp:
            resp.status = 300
            if resp.status in [403, 404]:

                # Для удобного логгирования
                url: str = str(resp.url)

                # Тело ответа запроса
                error_body = await safe_read_response(resp=resp)

                # Формируем дефолтные сообщения
                default_messages: Dict = {
                    403: "Доступ к сайту запрещен",
                    404: "Cервер не может найти запрошенный ресурс",
                }

                # Формируем ответ для пользователя
                error_message_str: str = (
                    error_body.get("message", default_messages[resp.status])
                    if isinstance(error_body, dict)
                    else default_messages[resp.status]
                )

                logg_error_str: str = str(error_body)[:500]

                # Формируем запись сообщения об ошибке в лог файл
                error_web_response_message: str = (
                    f"\n{'-' * 80}\nОшибка в {name_router}\nМетод: {resp.method}\n"
                    f"Status code: {resp.status}\nUrl: {url}\nТрессировка:\n"
                    f"{logg_error_str}\n{'-' * 80}"
                )

                error_logging.error(msg=error_web_response_message)

                return ResponseData(
                    status=resp.status,
                    error=error_message_str,
                    url=url,
                    method=method,
                )

            elif resp.status != 200:
                # Для удобного логгирования
                url: str = str(resp.url)
                error_body = await safe_read_response(resp=resp)

                logg_error_str: str = str(error_body)[:500]
                error_web_response_message: str = (
                    f"\n{'-' * 80}\nОшибка в {name_router}\nМетод: {resp.method}\n"
                    f"Status code:{resp.status}\nUrl:{url}\nТрессировка:\n"
                    f"{logg_error_str}\n{'-' * 80}"
                )
                error_logging.error(msg=error_web_response_message)

                return ResponseData(
                    STATUS=resp.status,
                    ERROR=f"Сайт вернул ошибку {resp.status}",
                    URL=url,
                    METHOD=method,
                )
            if data_type.upper() == "JSON":
                message_body = await resp.json()
                return ResponseData(
                    message=message_body,
                    status=resp.status,
                    url=url,
                    method=method,
                )
            elif data_type.upper() == "TEXT":
                message_body = await resp.text()
                return ResponseData(
                    message=message_body,
                    status=resp.status,
                    url=url,
                    method=method,
                )
            else:
                message_body = await resp.read()
                return ResponseData(
                    message=message_body,
                    status=resp.status,
                    url=url,
                    method=method,
                )
    except aiohttp.ClientError as err:
        error_logging.exception(msg=f"Ошибка сети при запросе {url}: {err}")
        return ResponseData(
            error=f"Произошла ошибка в сети при запросе на {url}",
            status=0,
            url=url,
            method=method,
        )
    except asyncio.TimeoutError as err:
        error_logging.exception(msg=f"Ожидание от сервера истекло {url}: {err}")
        return ResponseData(
            error=f"Время ожидания от сайта {url} истекло",
            status=0,
            url=url,
            method=method,
        )
    except Exception as err:
        error_logging.exception(f"Неизвестная ошибка при запросе {url}: {err}")
        return ResponseData(
            error="Ошибка на стороне сервера.Идет работа по исправлению...",
            status=0,
            url=url,
            method=method,
        )

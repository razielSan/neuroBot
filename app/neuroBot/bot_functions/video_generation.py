from typing import Optional, Callable, Dict
import time
import os
import base64
from logging import Logger
from random import choice

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver

from neuroBot.utils.selenium import create_selenium_driver
from neuroBot.extensions import chrome_selenium_settings
from core.response import ResponseData
from settings.response import messages
from erros_handlers.format import format_message
from neuroBot.extensions import video_gen_vheer_settings


def create_video_by_is_vheer(
    name_router: str,
    url: str,
    image_path: str,
    video_path: str,
    video_data: str,
    prompt: str,
    update_progress: Callable,
    error_logging: Logger,
    description_url: Optional[str] = None,
) -> Dict:

    """Заходит на сайт https://vheer.com, через  selenium, загружает описание
       изображений, жмет кнопку генерации видео и скачивае видео с сайта в папку

    Args:
        name_router (str): Имя роутера для записи в лог
        url (str): URL сайта vheer для генерации изображения
        image_path (str): Путь до картинки с изображением
        video_path (str): Путь для сохранения изображения
        video_data (str): JavsSripts для сохранения видео через blob
        prompt (str): описание изображения
        update_progress (Callable): Функция для отслеживания прогресса скачивания
        error_logging (Logger): Логгер для записи в лог файл
        description_url (str, Optional): URL для генерации описания изображения(str/None)
        None - По умолчанию

    Returns:
        ResponseData: Объект с результатом запроса.

        Атрибуты ResponseData:
            - message (Any | None): Данные успешного ответа (если запрос прошёл успешно).
            - error (str | None): Описание ошибки, если запрос завершился неудачей.
            - status (int): HTTP-код ответа. 0 — если ошибка возникла на клиентской стороне.
            - url (str): URL, по которому выполнялся запрос.
            - method (str): HTTP-метод, использованный при запросе.
    """

    driver = None
    try:

        # 1 Обновляем прогресс при заходе в функцию
        update_progress()

        # Создаем driver
        response_driver: ResponseData = create_selenium_driver(
            name_router=name_router,
            driver_path=chrome_selenium_settings.PATH_CHROME_DRIVER,
            add_arument=chrome_selenium_settings.LIST_ADD_ARGUMENT,
            error_logging=error_logging,
        )
        if response_driver.error:
            return response_driver
        driver = response_driver.message
        

        # 2 Обновляем прогресс(до загрузки сайта) для вывода пользователю
        update_progress()

        # Если есть URL для сайта с описанием изображения заходим в него
        if description_url:
            resonse_description: ResponseData = get_prompt_for_image_describepicture_сс(
                name_router=name_router,
                driver=driver,
                image_path=image_path,
                description_url=description_url,
                error_logging=error_logging,
            )

            # Если сайт по описанию изображения выдал ошибку используем стандартное описание
            if resonse_description.error:
                resonse_description.message = choice(
                    video_gen_vheer_settings.DEFAULT_LIST_DESCRIPTION_IMAGES,
                )
                update_progress(gen_description="default_description")
            else:
                update_progress(gen_description=True)

            prompt: str = resonse_description.message

        try:
            driver.get(url=url)
        except Exception as err:
            error_logging.exception(
                msg=format_message(
                    name_router=name_router,
                    method="GET",
                    status=0,
                    url=url,
                    error_text=f"Ошибка при доступе к сайту {url} - {err}",
                )
            )
            return ResponseData(
                error=messages.NETWORK_ERROR,
                url=url,
                status=0,
                method="GET",
            )

        # 3 Обновляем прогресс(когда сайт загрузился) для вывода пользователю
        update_progress()

        wait: WebDriverWait[WebElement] = WebDriverWait(driver, 60)

        # 4 Обновляем прогресс(до загрузки фото на сайт) для вывода пользователю
        update_progress()

        file_input: WebElement = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        abs_path: str = os.path.abspath(image_path)
        file_input.send_keys(abs_path)
        time.sleep(10)

        # 5 Обновляем прогресс(после загрузки фото на сайт загрузки сайта) для вывода пользователю
        update_progress()

        text_area: WebElement = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'textarea[placeholder^="Input image"]')
            )
        )
        text_area.clear()
        text_area.send_keys(prompt)
        time.sleep(2)

        # Ждём, пока overlay исчезнет (если есть блок Processing)
        try:
            wait.until(
                EC.invisibility_of_element_located(
                    (By.CSS_SELECTOR, "div.absolute.inset-0.z-20")
                )
            )
        except Exception:
            pass  # если overlay нет — игнорируем

        # Ждём появления кнопки и кликабельности
        button_generate: WebElement = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//text()[contains(., 'Generate')]]")
            )
        )

        # Скроллим и кликаем через JS (надёжнее на Tailwind/React)
        driver.execute_script("arguments[0].scrollIntoView(true);", button_generate)
        driver.execute_script("arguments[0].click();", button_generate)
        time.sleep(2)

        # 6 Обновляем прогресс(после того когда кликнули кнопку сгенерировать видео) для вывода пользователю
        update_progress()

        # Ждём появления <video> — сайт сначала генерирует blob, поэтому даём запас времени
        video_el: WebElement = WebDriverWait(driver, 400).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.h-full.relative > video")
            )
        )

        # 7 Обновляем прогресс(после того когда видео сгенерировалось) для вывода пользователю
        update_progress()

        # settings.video_generation.vheer.VIDEO_DATA,

        # Достаём blob как base64 через JavaScript
        video_data: str = driver.execute_async_script(
            video_data,
            video_el,
        )

        if video_data.startswith("ERROR:"):
            driver.quit()
            return ResponseData(
                error="Не удалось скачать видео: " + video_data,
                url=url,
                status=200,
                method="GET",
            )

        # Сохраняем base64 как mp4
        header, encoded = video_data.split(",", 1)
        binary_data: bytes = base64.b64decode(encoded)

        # 8 Обновляем прогресс(до того когда сохранили видео в папку) для вывода пользователю
        update_progress()

        # Загружаем картинку в путь
        with open(video_path, "wb") as f:
            f.write(binary_data)

        # 9 Обновляем прогресс(когда сохранили видео в папку) для вывода пользователю
        update_progress()

        return ResponseData(
            message="Видео успешно загружено",
            url=url,
            method="GET",
            status=200,
        )

    except Exception as err:
        error_logging.exception(
            msg=format_message(
                name_router=name_router,
                method="<unknown>",
                status=0,
                url=description_url,
                error_text=err,
            )
        )
        return ResponseData(
            error=messages.NETWORK_ERROR,
            url=url,
            status=0,
            method="<unknown>",
        )
    finally:
        if driver:
            try:
                driver.quit()
            except Exception:
                pass


def get_prompt_for_image_by_produts_appose_ai(
    name_router: str,
    driver: webdriver.Chrome,
    image_path: str,
    description_url: str,
    error_logging: Logger,
) -> ResponseData:
    """Заходит на сайт "https://products.aspose.ai, загружает картинку, нажимает на кнопку сгенерировать
    описание и возвращает описание изображения

    Args:
        name_router (str): Имя роутера для записи в лог
        driver (_type_): драйвер для селениума
        image_path (str): путь до картинки для описания
        description_url (str): URL сайта для описания изображения
        error_logging (Logger): логгер для записи в лог файл

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
        # Переходим по ссылке
        driver.get(description_url)

        wait: WebDriverWait = WebDriverWait(driver, 60)

        # Загружаем картинку на сайт
        image_input: WebElement = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        path: str = os.path.abspath(image_path)
        image_input.send_keys(path)
        time.sleep(2)

        # Выбираем английский язык для описания
        wait.until(EC.visibility_of_element_located((By.ID, "description-lang")))
        Select(driver.find_element(By.ID, "description-lang")).select_by_value("en")
        time.sleep(2)

        # Кликаес на кнопку
        generate_button: WebElement = wait.until(
            EC.presence_of_element_located((By.ID, "uploadButton"))
        )
        generate_button.click()

        # Ждем описания изображения
        text_area: WebElement = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "textarea[class='text-area']",
                )
            )
        )

        text: str = text_area.text.translate(str.maketrans("", "", "*-"))

        return ResponseData(
            message=text,
            url=description_url,
            method="GET",
            status=200,
        )
    except Exception as err:
        error_logging.exception(
            msg=format_message(
                name_router=name_router,
                method="<unknown>",
                status=0,
                url=description_url,
                error_text=err,
            )
        )
        return ResponseData(
            error=messages.NETWORK_ERROR,
            url=description_url,
            status=0,
            method="<unknown>",
        )


def get_prompt_for_image_describepicture_сс(
    name_router: str,
    driver: webdriver.Chrome,
    image_path: str,
    description_url: str,
    error_logging: Logger,
) -> ResponseData:
    """
        Заходит на сайт "https://describepicture.cc/ru, загружает
        картинку, нажимает на кнопку сгенерировать
        описание и возвращает описание изображения

    Args:
        name_router (str): Имя роутера для записи в лог
        driver (_type_): драйвер для селениума
        image_path (str): путь до картинки для описания
        description_url (str): URL сайта для описания изображения
        error_logging (Logger): логгер для записи в лог файл

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
        # Заходит на сайт
        driver.get(description_url)
        # Ждет пока не прогрузийтся страница

        wait: WebDriverWait = WebDriverWait(driver, 60)

        # Загружает картинку на сайт
        image_input: WebElement = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        path: str = os.path.abspath(image_path)
        image_input.send_keys(path)

        # Ждем чтобы картинка прогрузилась
        time.sleep(5)

        # Кликаем по кнопке с генерацие описания
        generate_button = driver.find_element(
            By.CSS_SELECTOR, "button[class*='bg-gradient-to-r']"
        )
        generate_button.click()

        # Ждем 10 секунд чтобы генерация завершилась
        time.sleep(10)

        # Достаем текст описания изображения
        text_area: WebElement = wait.until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "textarea[class*='rounded-lg']",
                )
            )
        )

        return ResponseData(
            message=text_area.text,
            url=description_url,
            method="GET",
            status=200,
        )
    except Exception as err:
        error_logging.exception(
            msg=format_message(
                name_router=name_router,
                method="<unknown>",
                status=0,
                url=description_url,
                error_text=err,
            )
        )
        return ResponseData(
            error=messages.NETWORK_ERROR,
            url=description_url,
            status=0,
            method="<unknown>",
        )

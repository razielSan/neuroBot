import base64

from aiohttp import ClientSession

from erros_handlers.main import error_handler_for_the_website
from core.response import LoggingData, ResponseData


async def get_and_save_image(
    url: str,
    path_img: str,
    session: ClientSession,
    logging_data: LoggingData,
    gpt_image_1=None,
) -> ResponseData:
    """_summary_

    Args:
        url (str): _description_
        path_img (str): _description_
        session (ClientSession): _description_
        logging_data (LoggingData): _description_
        gpt_image_1 (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    # try:
    if gpt_image_1:
        image_file = base64.b64decode(url)
        with open(path_img, "wb") as image:
            image.write(image_file)
    else:
        # Делаем запрос на сайт для получения данных о картинке
        response: ResponseData = await error_handler_for_the_website(
            session=session,
            url=url,
            logging_data=logging_data,
            data_type="BYTES",
            timeout=120,
            function_name=get_and_save_image.__name__
        )

        if response.error:
            return response

        # Сохраняем картинку по переданному пути
        with open(path_img, "wb") as file:
            file.write(response.message)

    return ResponseData(
        message=path_img,
        url=url,
        method="GET",
        status=200,
    )

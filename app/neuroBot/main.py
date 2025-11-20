import aiohttp

from neuroBot.extensions import (
    bot,
    dp,
    bot_settings,
    model_settings,
    neurobot_main_logger,
)


from neuroBot.views import main_router
from neuroBot.views.image_description import image_description_router
from neuroBot.views.image_generation import image_generation_router
from neuroBot.views.video_generation import video_generation_router
from utils.filesistem import ensure_derictories


# Создаем небходимые папки
ensure_derictories(
    bot_settings.PATH_BOT_STATIC_FOLDER,
    bot_settings.PATH_BOT_TEMP_FOLDER,
    model_settings.img_desc_models.imagga.PATH_TO_IMAGES,
    model_settings.video_gen_models.vheer.PATH_TO_IMAGES,
    model_settings.video_gen_models.vheer.PATH_TO_VIDEO,
    model_settings.img_gen_models.pollinations.PATH_TO_IMAGES,
    model_settings.img_gen_models.caila.PATH_TO_IMAGES,
    model_settings.img_gen_models.stablehorde.PATH_TO_IMAGES,
    model_settings.img_gen_models.vheer.PATH_TO_IMAGES,
    # info_logger=neurobot_main_logger.info_logger,
)


async def run_bot() -> None:
    """Подлючает все параметры для бота и запускает его."""
    # Встаем в try/except чтобы отловить все что не попало в middleware
    try:
        await bot.set_my_commands(
            commands=bot_settings.LIST_BOT_COMMANDS
        )  # Добавляет команды боту
        await bot.delete_webhook(
            drop_pending_updates=True
        )  # Игнорирует все присланные сообщение пока бот не работал

        # Подключаем роутеры
        dp.include_router(video_generation_router)
        dp.include_router(image_generation_router)
        dp.include_router(image_description_router)
        dp.include_router(main_router)

        # Создаем глобальную сессию для всего бота. Будет доступ в роутерах через
        # название указанное ниже

        neurobot_main_logger.info_logger.info(f"{bot_settings.BOT_NAME} запущен")
        async with aiohttp.ClientSession() as session:
            dp["session"] = session
            await dp.start_polling(bot)
    except Exception as err:
        neurobot_main_logger.error_logger.exception(
            f"Критическая ошибка при работа бота {bot_settings.BOT_NAME}: {err}"
        )

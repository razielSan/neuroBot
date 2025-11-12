from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.image_description.main import image_description_router
from neuroBot.views.image_description.imagga import imagga_img_desc_router
from neuroBot.extensions import neurobot_image_description_logger
from neuroBot.extensions import neurobot_main_logger


image_description_router.include_router(imagga_img_desc_router)


image_description_router.message.middleware(
    RouterErrorMiddleware(
        neurobot_image_description_logger.error_logger,
        neurobot_main_logger.error_logger
    )
)
image_description_router.callback_query.middleware(
    RouterErrorMiddleware(
        neurobot_image_description_logger.error_logger,
        neurobot_main_logger.error_logger
    )
)

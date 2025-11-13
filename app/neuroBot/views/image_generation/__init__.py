from neuroBot.extensions import neurobot_image_generation_logger, neurobot_main_logger
from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.image_generation.main import image_generation_router
from neuroBot.views.image_generation.pollinations import pollinations_img_gen_router


image_generation_router.include_router(pollinations_img_gen_router)


image_generation_router.message.middleware(
    RouterErrorMiddleware(
        neurobot_image_generation_logger.error_logger,
        neurobot_main_logger.error_logger,
    )
)
image_generation_router.callback_query.middleware(
    RouterErrorMiddleware(
        neurobot_image_generation_logger.error_logger,
        neurobot_main_logger.error_logger,
    )
)

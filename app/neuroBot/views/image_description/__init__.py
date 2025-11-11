from neuroBot.extensions import logging_data
from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.image_description.main import image_description_router
from neuroBot.views.image_description.imagga import imagga_img_desc_router


image_description_router.include_router(imagga_img_desc_router)


image_description_router.message.middleware(
    RouterErrorMiddleware(
        logging_data.BOT_ROUTER_NAME["image_description"].error_logger,
        logging_data.BOT_ROUTER_NAME["neuroBot"].error_logger,
    )
)
image_description_router.callback_query.middleware(
    RouterErrorMiddleware(
        logging_data.BOT_ROUTER_NAME["image_description"].error_logger,
        logging_data.BOT_ROUTER_NAME["neuroBot"].error_logger,
    )
)

from neuroBot.extensions import logging_data
from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.image_generation.main import image_generation_router


image_generation_router.message.middleware(
    RouterErrorMiddleware(
        logging_data.BOT_ROUTER_NAME["image_generation"].error_logger,
        logging_data.BOT_ROUTER_NAME["neuroBot"].error_logger,
    )
)
image_generation_router.callback_query.middleware(
    RouterErrorMiddleware(
        logging_data.BOT_ROUTER_NAME["image_generation"].error_logger,
        logging_data.BOT_ROUTER_NAME["neuroBot"].error_logger,
    )
)

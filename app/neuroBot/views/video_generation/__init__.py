from neuroBot.extensions import logging_data
from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.video_generation.main import video_generation_router
from neuroBot.views.video_generation.vheer import vheer_router


video_generation_router.include_router(vheer_router)

video_generation_router.message.middleware(
    RouterErrorMiddleware(
        logging_data.BOT_ROUTER_NAME["video_generation"],
        logging_data.BOT_ROUTER_NAME["neuroBot"].error_logger,
    )
)
video_generation_router.callback_query.middleware(
    RouterErrorMiddleware(
        logging_data.BOT_ROUTER_NAME["video_generation"].error_logger,
        logging_data.BOT_ROUTER_NAME["neuroBot"].error_logger,
    )
)

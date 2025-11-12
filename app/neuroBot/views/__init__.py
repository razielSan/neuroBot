from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.main import main_router

from neuroBot.extensions import neurobot_main_logger


main_router.message.middleware(
    RouterErrorMiddleware(
        neurobot_main_logger.error_logger
    )
)

main_router.callback_query.middleware(
    RouterErrorMiddleware(
        neurobot_main_logger,
    )
)

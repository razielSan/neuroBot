from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.main import main_router

from neuroBot.extensions import error_logger


main_router.message.middleware(
    RouterErrorMiddleware(
        logger=error_logger,
    )
)

main_router.callback_query.middleware(
    RouterErrorMiddleware(
        logger=error_logger,
    )
)

from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.main import main_router

from neuroBot.extensions import logging_data


main_router.message.middleware(
    RouterErrorMiddleware(
        logger=logging_data.BOT_ROUTER_NAME["neuroBot"].error_logger,
    )
)

main_router.callback_query.middleware(
    RouterErrorMiddleware(
       logger=logging_data.BOT_ROUTER_NAME["neuroBot"].error_logger,
    )
)

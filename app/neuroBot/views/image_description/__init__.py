from neuroBot.extensions import image_description_error_logger, error_logger
from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.image_description.main import image_description_router


image_description_router.message.middleware(
    RouterErrorMiddleware(
        image_description_error_logger,
        error_logger,
    )
)
image_description_router.callback_query.middleware(
    RouterErrorMiddleware(
        image_description_error_logger,
        error_logger,
    )
)

from neuroBot.extensions import image_generation_error_logger, error_logger
from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.image_generation.main import image_generation_router


image_generation_router.message.middleware(
    RouterErrorMiddleware(
        image_generation_error_logger,
        error_logger,
    )
)
image_generation_router.callback_query.middleware(
    RouterErrorMiddleware(
        image_generation_error_logger,
        error_logger,
    )
)

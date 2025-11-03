from neuroBot.extensions import video_generation_error_logger, error_logger
from neuroBot.middleware.errors_middleware import RouterErrorMiddleware
from neuroBot.views.video_generation.main import video_generation_router


video_generation_router.message.middleware(
    RouterErrorMiddleware(
        video_generation_error_logger,
        error_logger,
    )
)
video_generation_router.callback_query.middleware(
    RouterErrorMiddleware(
        video_generation_error_logger,
        error_logger,
    )
)

from ninja import NinjaAPI
from shared.domain.errors import DomainError


class ErrorHandlerAdater:
    """Represents an adapter of error handler."""

    def __init__(self, router: NinjaAPI):
        self.router = router

        @router.exception_handler(DomainError)
        def on_domain_error(request, exc):
            data = {
                "client_message": str(exc),
            }
            return router.create_response(
                request=request,
                data=data,
                status=exc.status_code,
            )

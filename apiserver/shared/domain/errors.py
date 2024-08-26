class DomainError(Exception):
    """Represents a error of domain or application."""

    def __init__(self, message=None):
        self.message = self.message if message is None else message
        super().__init__(self.status_code, self.message)

    def __str__(self) -> str:
        return f"[{self.status_code}]: {self.message}"


class BadRequestError(DomainError):
    """Represents a error of bad request from client."""

    message = "bad request"
    status_code = 400

    def __init__(self, message=None):
        super().__init__(message)


class UnauthorizedError(DomainError):
    """Represents a error of unauthorized."""

    message = "unauthorized"
    status_code = 401

    def __init__(self, message=None):
        super().__init__(message)


class ForbiddenError(DomainError):
    """Represents a error of forbidden."""

    message = "forbidden"
    status_code = 403

    def __init__(self, message=None):
        super().__init__(message)


class NotFoundError(DomainError):
    """Represents a error of not found."""

    message = "not found"
    status_code = 404

    def __init__(self, message=None):
        super().__init__(message)


class ConflictError(DomainError):
    """Represents a error of conflict."""

    message = "conflict"
    status_code = 409

    def __init__(self, message=None):
        super().__init__(message)


class UnprocessableEntityError(DomainError):
    """Represents a error of unprocessable entity."""

    message = "unprocessable entity"
    status_code = 422

    def __init__(self, message=None):
        super().__init__(message)


class TooManayRequestError(DomainError):
    """Represents a error of too many request."""

    message = "too many request"
    status_code = 429

    def __init__(self, message=None):
        super().__init__(message)


class InternalServerError(DomainError):
    """Represents a error of unprocessable entity."""

    message = "internal server"
    status_code = 500

    def __init__(self, message=None):
        super().__init__(message)

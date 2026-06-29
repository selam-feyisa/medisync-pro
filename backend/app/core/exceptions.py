"""Exception classes for API error handling."""


class APIException(Exception):
    """Base API exception."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class ValidationError(APIException):
    """Validation error exception."""

    def __init__(self, detail: str):
        super().__init__(400, detail)


class AuthenticationError(APIException):
    """Authentication error exception."""

    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(401, detail)


class AuthorizationError(APIException):
    """Authorization error exception."""

    def __init__(self, detail: str = "Not authorized"):
        super().__init__(403, detail)


class NotFoundError(APIException):
    """Resource not found exception."""

    def __init__(self, detail: str):
        super().__init__(404, detail)


class ConflictError(APIException):
    """Resource conflict exception."""

    def __init__(self, detail: str):
        super().__init__(409, detail)


class RateLimitError(APIException):
    """Rate limit exceeded exception."""

    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(429, detail)


ValidationException = ValidationError
NotFoundException = NotFoundError
PermissionException = AuthorizationError

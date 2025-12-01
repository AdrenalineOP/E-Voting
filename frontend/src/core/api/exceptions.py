"""API exceptions."""


class APIException(Exception):
    """Base API exception."""

    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}
        super().__init__(self.message)


class AuthenticationError(APIException):
    """Authentication failed (401)."""
    pass


class AuthorizationError(APIException):
    """Authorization failed (403)."""
    pass


class ValidationError(APIException):
    """Validation error (422)."""
    pass


class NotFoundError(APIException):
    """Resource not found (404)."""
    pass


class ServerError(APIException):
    """Server error (5xx)."""
    pass


class NetworkError(APIException):
    """Network/connection error."""

    def __init__(self, message: str):
        super().__init__(message, status_code=None, response_data={})


class TokenExpiredError(APIException):
    """Token expired error."""
    pass


class EmailAlreadyExistsError(APIException):
    """Email already exists error."""

    def __init__(self, message: str, email: str, response_data: dict = None):
        super().__init__(message, status_code=422, response_data=response_data)
        self.email = email

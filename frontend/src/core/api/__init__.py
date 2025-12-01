"""API client package."""
from .client import APIClient
from .organizations import OrganizationsAPI
from .otp import OTPAPI
from .exceptions import (
    APIException,
    AuthenticationError,
    AuthorizationError,
    ValidationError,
    NotFoundError,
    ServerError,
    NetworkError,
    TokenExpiredError,
    EmailAlreadyExistsError,
)


class API:
    """Main API wrapper combining all endpoints."""

    def __init__(self, storage=None):
        """Initialize API.

        Args:
            storage: Storage instance for managing tokens
        """
        self.client = APIClient(storage)

        # Initialize endpoint groups
        self.organizations = OrganizationsAPI(self.client)
        self.otp = OTPAPI(self.client)

    def close(self):
        """Close API client."""
        self.client.close()


# Export main classes
__all__ = [
    "API",
    "APIClient",
    "OrganizationsAPI",
    "OTPAPI",
    "APIException",
    "AuthenticationError",
    "AuthorizationError",
    "ValidationError",
    "NotFoundError",
    "ServerError",
    "NetworkError",
    "TokenExpiredError",
    "EmailAlreadyExistsError",
]

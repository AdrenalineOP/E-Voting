"""Base API client with authentication and error handling."""

import httpx

from typing import Optional, Dict, Any

from ..config import api_config

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


class APIClient:
    """Base API client for making HTTP requests."""

    def __init__(self, storage=None):
        """Initialize API client.

        Args:
            storage: Storage instance for managing tokens
        """
        self.base_url = api_config.api_url
        self.storage = storage
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=httpx.Timeout(api_config.TIMEOUT, connect=api_config.CONNECT_TIMEOUT),
            follow_redirects=True,
        )

    def _get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Get request headers with optional authentication.

        Args:
            include_auth: Whether to include Authorization header

        Returns:
            Headers dictionary
        """
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if include_auth and self.storage:
            access_token = self.storage.get("access_token")
            if access_token:
                headers["Authorization"] = f"Bearer {access_token}"

        return headers

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions.

        Args:
            response: HTTP response object

        Returns:
            Response JSON data

        Raises:
            Various APIException subclasses based on status code
        """
        try:
            data = response.json()
        except Exception:
            data = {"detail": response.text}

        # Success responses
        if 200 <= response.status_code < 300:
            return data

        # Error responses
        error_message = data.get("detail", "An error occurred")

        # Check for email already exists error (400 OR 422 with specific error code)
        if response.status_code in [400, 422]:
            # Handle dict detail (FastAPI validation error format)
            if isinstance(error_message, dict):
                error_code = error_message.get("error")
                if error_code == "email_already_exists":
                    email = error_message.get("field", "")
                    message = error_message.get("message", "Email already exists")
                    raise EmailAlreadyExistsError(message, email, data)

            # Regular validation error
            if response.status_code == 400:
                raise ValidationError(str(error_message), response.status_code, data)
            raise ValidationError(str(error_message), response.status_code, data)

        if response.status_code == 401:
            # Check if token expired
            if "expired" in str(error_message).lower():
                raise TokenExpiredError(str(error_message), response.status_code, data)
            raise AuthenticationError(str(error_message), response.status_code, data)

        elif response.status_code == 403:
            raise AuthorizationError(str(error_message), response.status_code, data)

        elif response.status_code == 404:
            raise NotFoundError(str(error_message), response.status_code, data)

        elif response.status_code >= 500:
            raise ServerError(str(error_message), response.status_code, data)

        else:
            raise APIException(str(error_message), response.status_code, data)

    def get(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            include_auth: bool = True,
    ) -> Dict[str, Any]:
        """Make GET request."""
        try:
            response = self.client.get(
                endpoint,
                params=params,
                headers=self._get_headers(include_auth),
            )
            return self._handle_response(response)
        except httpx.ConnectError as e:
            raise NetworkError(f"Failed to connect to server: {str(e)}")
        except httpx.TimeoutException as e:
            raise NetworkError(f"Request timeout: {str(e)}")

    def post(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            files: Optional[Dict[str, Any]] = None,
            include_auth: bool = True,
    ) -> Dict[str, Any]:
        """Make POST request."""
        try:
            headers = self._get_headers(include_auth)
            # Remove Content-Type if uploading files
            if files:
                headers.pop("Content-Type", None)

            response = self.client.post(
                endpoint,
                data=data,
                json=json,
                files=files,
                headers=headers,
            )
            return self._handle_response(response)
        except httpx.ConnectError as e:
            raise NetworkError(f"Failed to connect to server: {str(e)}")
        except httpx.TimeoutException as e:
            raise NetworkError(f"Request timeout: {str(e)}")

    def put(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            include_auth: bool = True,
    ) -> Dict[str, Any]:
        """Make PUT request."""
        try:
            response = self.client.put(
                endpoint,
                data=data,
                json=json,
                headers=self._get_headers(include_auth),
            )
            return self._handle_response(response)
        except httpx.ConnectError as e:
            raise NetworkError(f"Failed to connect to server: {str(e)}")
        except httpx.TimeoutException as e:
            raise NetworkError(f"Request timeout: {str(e)}")

    def delete(
            self,
            endpoint: str,
            include_auth: bool = True,
    ) -> Dict[str, Any]:
        """Make DELETE request."""
        try:
            response = self.client.delete(
                endpoint,
                headers=self._get_headers(include_auth),
            )
            return self._handle_response(response)
        except httpx.ConnectError as e:
            raise NetworkError(f"Failed to connect to server: {str(e)}")
        except httpx.TimeoutException as e:
            raise NetworkError(f"Request timeout: {str(e)}")

    def close(self):
        """Close HTTP client."""
        self.client.close()

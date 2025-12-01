"""Application configuration."""
from pydantic import BaseModel


class APIConfig(BaseModel):
    """API configuration."""

    # Backend server URL
    BASE_URL: str = "http://localhost:8000"  # Change to your server IP

    # Timeouts (in seconds)
    TIMEOUT: int = 15
    CONNECT_TIMEOUT: int = 15

    # Retry configuration
    MAX_RETRIES: int = 3

    @property
    def api_url(self) -> str:
        """Get full API URL."""
        return f"{self.BASE_URL}/api"


# Global configuration instance
api_config = APIConfig()

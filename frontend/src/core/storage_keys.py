"""Client storage key constants for type safety."""
from enum import Enum


class StorageKey(str, Enum):
    """Client storage keys used throughout the application."""

    # Initialization
    IS_INITIALIZED = "is_initialized"

    # Window preferences
    WINDOW_MAXIMIZED = "window_maximized"
    PREVENT_CLOSE_DIALOG = "prevent_close_dialog"

    # Application data
    ORGANIZATION_ID = "organization_id"
    SYSTEM_ID = "system_id"
    APP_VERSION = "app_version"
    CREATED_AT = "created_at"

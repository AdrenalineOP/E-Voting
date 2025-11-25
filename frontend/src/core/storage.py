"""Client storage management with safe defaults."""
import flet as ft
from typing import Any

from datetime import datetime
from .storage_keys import StorageKey

# Default values for all storage keys (no None values!)
STORAGE_DEFAULTS = {
    # Initialization
    StorageKey.IS_INITIALIZED: False,

    # Window preferences
    StorageKey.WINDOW_MAXIMIZED: True,
    StorageKey.PREVENT_CLOSE_DIALOG: True,

    # Application data (use empty strings instead of None)
    StorageKey.ORGANIZATION_ID: "",
    StorageKey.SYSTEM_ID: "",
    StorageKey.APP_VERSION: "7.01",
    StorageKey.CREATED_AT: "",
}


class ClientStorage:
    """Wrapper for Flet client storage with safe defaults."""

    def __init__(self, page: ft.Page):
        self.page = page
        self._storage = page.client_storage

    def initialize(self) -> None:
        """Initialize all storage keys with defaults on first run."""
        if not self.contains(StorageKey.IS_INITIALIZED):
            # First run - set all defaults
            for key, value in STORAGE_DEFAULTS.items():
                self.set(key, value)

            # Set initialization timestamp
            self.set(StorageKey.CREATED_AT, datetime.now().isoformat())
            self.set(StorageKey.IS_INITIALIZED, True)

    def get(self, key: StorageKey, default: Any = None) -> Any:
        """Safely get value from storage with fallback.

        Args:
            key: Storage key (use StorageKey enum)
            default: Default value if key doesn't exist or is None

        Returns:
            Stored value or default
        """
        # Convert enum to string for storage access
        key_str = str(key.value)

        if not self._storage.contains_key(key_str):
            return default if default is not None else STORAGE_DEFAULTS.get(key)

        value = self._storage.get(key_str)

        # Return empty string as None for application data fields
        if value == "" and key in [StorageKey.ORGANIZATION_ID, StorageKey.SYSTEM_ID]:
            return None

        return value if value is not None else (
            default if default is not None else STORAGE_DEFAULTS.get(key)
        )

    async def get_async(self, key: StorageKey, default: Any = None) -> Any:
        """Async version of get for use in async contexts.

        Args:
            key: Storage key (use StorageKey enum)
            default: Default value if key doesn't exist or is None

        Returns:
            Stored value or default
        """
        # Convert enum to string for storage access
        key_str = str(key.value)

        if not await self._storage.contains_key_async(key_str):
            return default if default is not None else STORAGE_DEFAULTS.get(key)

        value = await self._storage.get_async(key_str)

        # Return empty string as None for application data fields
        if value == "" and key in [StorageKey.ORGANIZATION_ID, StorageKey.SYSTEM_ID]:
            return None

        return value if value is not None else (
            default if default is not None else STORAGE_DEFAULTS.get(key)
        )

    def set(self, key: StorageKey, value: Any) -> None:
        """Set value in storage.

        Args:
            key: Storage key (use StorageKey enum)
            value: Value to store (cannot be None)
        """
        # Convert enum to string for storage access
        key_str = str(key.value)

        # Convert None to empty string for storage
        if value is None:
            value = ""

        self._storage.set(key_str, value)

    async def set_async(self, key: StorageKey, value: Any) -> None:
        """Async version of set for use in async contexts.

        Args:
            key: Storage key (use StorageKey enum)
            value: Value to store (cannot be None)
        """
        # Convert enum to string for storage access
        key_str = str(key.value)

        # Convert None to empty string for storage
        if value is None:
            value = ""

        await self._storage.set_async(key_str, value)

    def contains(self, key: StorageKey) -> bool:
        """Check if key exists in storage.

        Args:
            key: Storage key to check

        Returns:
            True if key exists, False otherwise
        """
        # Convert enum to string for storage access
        key_str = str(key.value)
        return self._storage.contains_key(key_str)

    async def contains_async(self, key: StorageKey) -> bool:
        """Async version of contains for use in async contexts.

        Args:
            key: Storage key to check

        Returns:
            True if key exists, False otherwise
        """
        # Convert enum to string for storage access
        key_str = str(key.value)
        return await self._storage.contains_key_async(key_str)

    def remove(self, key: StorageKey) -> None:
        """Remove key from storage.

        Args:
            key: Storage key to remove
        """
        key_str = str(key.value)
        if self._storage.contains_key(key_str):
            self._storage.remove(key_str)

    def clear(self) -> None:
        """Clear all storage data."""
        self._storage.clear()

    def is_first_launch(self) -> bool:
        """Check if this is the first application launch.

        Returns:
            True if organization_id is not set
        """
        org_id = self.get(StorageKey.ORGANIZATION_ID)
        # Empty string or None means not set
        return not org_id or org_id == ""

    async def is_first_launch_async(self) -> bool:
        """Async version of is_first_launch for use in async contexts.

        Returns:
            True if organization_id is not set
        """
        org_id = await self.get_async(StorageKey.ORGANIZATION_ID)
        # Empty string or None means not set
        return not org_id or org_id == ""

"""Application initialization and setup."""
from core.storage import ClientStorage
from core.storage_keys import StorageKey


def initialize_app(storage: ClientStorage) -> None:
    """Initialize application storage and check first launch.

    Args:
        storage: ClientStorage instance
    """
    # Initialize all storage keys with defaults
    storage.initialize()

    # Check if this is first launch
    if storage.is_first_launch():
        print("FIRST LAUNCH DETECTED")
    else:
        print("EXISTING INSTALLATION")

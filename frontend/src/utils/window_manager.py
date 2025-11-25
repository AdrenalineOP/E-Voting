"""Window event management and handlers."""
import flet as ft
from core.storage import ClientStorage
from core.storage_keys import StorageKey
from ui.dialogs.exit_dialog import show_exit_dialog


def setup_window(page: ft.Page, storage: ClientStorage) -> None:
    """Setup window event handlers and initial state.

    Args:
        page: Flet page instance
        storage: ClientStorage instance
    """
    # Get window preferences from storage
    prevent_close = storage.get(StorageKey.PREVENT_CLOSE_DIALOG)
    is_maximized = storage.get(StorageKey.WINDOW_MAXIMIZED)

    # Configure window
    page.window.prevent_close = prevent_close
    page.window.maximized = is_maximized

    # Register event handlers
    page.window.on_event = lambda e: handle_window_event(page, storage, e)


def handle_window_event(page: ft.Page, storage: ClientStorage, event: ft.EventType) -> None:
    """Handle window events (close, resize, etc.).

    Args:
        page: Flet page instance
        storage: ClientStorage instance
        event: Window event
    """
    if event.data == "close":
        # Check if we should show exit confirmation
        prevent_close = storage.get(StorageKey.PREVENT_CLOSE_DIALOG)
        if prevent_close:
            show_exit_dialog(page, storage)
        else:
            page.window.destroy()
    elif event.data == "resized":
        # Handle resize/maximize events
        handle_resize(page, storage)


def handle_resize(page: ft.Page, storage: ClientStorage) -> None:
    """Handle window resize events and save state.

    Args:
        page: Flet page instance
        storage: ClientStorage instance
    """
    try:
        current_maximized = page.window.maximized
        stored_maximized = storage.get(StorageKey.WINDOW_MAXIMIZED)

        # Only update if state changed
        if current_maximized != stored_maximized:
            storage.set(StorageKey.WINDOW_MAXIMIZED, current_maximized)
            page.update()
    except (ValueError, AttributeError) as e:
        print(f"Window resize error: {e}")

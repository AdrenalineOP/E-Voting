"""E-Voting Application - Main Entry Point"""
import flet as ft
from core import ClientStorage, StorageKey
from ui.theme import configure_theme
from utils.window_manager import setup_window
from ui.page import StartMenuPage
from ui.components import create_glass_container, create_content_layout, create_background_container


def main(page: ft.Page) -> None:
    """Main application entry point.

    Args:
        page: Flet page instance
    """
    # Initialize storage
    storage = ClientStorage(page)
    storage.initialize()

    # Configure window
    version = storage.get(StorageKey.APP_VERSION)
    page.title = f"E-Voting - v{version}"
    page.window.min_width = 900
    page.window.min_height = 700
    page.window.center()

    # Setup window behavior and theme
    setup_window(page, storage)
    configure_theme(page)

    # Create and render main layout
    _render_main_layout(page, storage)


def _render_main_layout(page: ft.Page, storage: ClientStorage) -> None:
    """Render main application layout.

    Args:
        page: Flet page instance
        storage: Storage manager
    """
    # Create content layout
    content_image, content_column = create_content_layout(
        image_height=370,
        image_src="/images/content_image-1.png",
    )

    # Create glass container with content
    glass_container = create_glass_container(
        content=ft.Column(
            [content_image, content_column],
            width=450,
            height=550,
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=450,
        height=550,
    )

    # Create background container
    bg_container = create_background_container(
        content=glass_container,
        background_image="/images/Background-1.png",
    )

    # Add to page
    page.add(bg_container)

    # Render start menu
    start_menu = StartMenuPage(page, content_image, content_column, storage)
    start_menu.render()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")

"""E-Voting Application - Main Entry Point"""
import flet as ft
from core import ClientStorage, StorageKey
from services.initialization import initialize_app
from ui.theme import configure_theme
from utils.window_manager import setup_window


def main(page: ft.Page) -> None:
    """Main application entry point.

    Args:
        page: Flet page instance
    """
    # Initialize storage wrapper
    storage = ClientStorage(page)

    # Initialize app and storage on first run
    initialize_app(storage)

    # Configure window
    page.title = f"E-Voting - {storage.get(StorageKey.APP_VERSION)}"
    page.window_min_width = 900
    page.window_min_height = 700
    page.window.center()

    # Setup window behavior
    setup_window(page, storage)

    # Apply theme and fonts
    configure_theme(page)

    content_image = ft.Container(
        image=ft.DecorationImage(
            src='/images/content_image-1.png',
            fit=ft.ImageFit.FIT_HEIGHT
        ),
        height=370,
        animate=ft.Animation(600, ft.AnimationCurve.DECELERATE)
    )

    content_column = ft.Column(
        width=450,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    bg_container = ft.Container(
        image=ft.DecorationImage(
            src="/images/Background-1.png",
            fit=ft.ImageFit.COVER
        ),
        margin=-10,
        alignment=ft.alignment.center,
        expand=True,
        content=ft.Container(
            width=450,
            height=550,
            border_radius=15,
            bgcolor='#44CCCCCC',
            blur=ft.Blur(30, 15, ft.BlurTileMode.MIRROR),
            content=ft.Column(
                [
                    content_image,
                    content_column,
                ],
                width=450,
                height=550,
            )
        )
    )

    page.add(bg_container)
    # start_menu_page(page, content_image, content_column, storage)


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")


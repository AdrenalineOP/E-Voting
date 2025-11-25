"""UI theme and font configuration."""
import flet as ft

def configure_fonts(page: ft.Page) -> None:
    """Configure custom fonts for the application.

    Args:
        page: Flet page instance
    """
    page.fonts = {
        "SpaceGrotesk": "/fonts/SpaceGrotesk.ttf",
    }


def configure_theme(page: ft.Page) -> None:
    """Configure application theme and fonts.

    Args:
        page: Flet page instance
    """
    # Configure fonts first
    configure_fonts(page)

    # Apply theme mode
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed='indigo',
        font_family='SpaceGrotesk',
    )

    # Update page
    page.update()

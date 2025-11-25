"""Reusable layout components."""
import flet as ft


def create_glass_container(content: ft.Control, width: int, height: int) -> ft.Container:
    """Create a glassmorphism container."""
    return ft.Container(
        width=width,
        height=height,
        border_radius=15,
        bgcolor='#44CCCCCC',
        blur=ft.Blur(25, 10, ft.BlurTileMode.MIRROR),
        content=content,
    )


def create_content_layout(image_height: int, image_src: str) -> tuple[ft.Container, ft.Column]:
    """Create content image and column layout."""
    content_image = ft.Container(
        image=ft.DecorationImage(
            src=image_src,
            fit=ft.ImageFit.FIT_HEIGHT,
        ),
        height=image_height,
        animate=ft.Animation(600, ft.AnimationCurve.DECELERATE),
    )

    content_column = ft.Column(
        width=450,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
    )

    return content_image, content_column


def create_background_container(content: ft.Control, background_image: str) -> ft.Container:
    """Create background container with image.

    Args:
        content: Content to display
        background_image: Background image path

    Returns:
        Container with background image
    """
    return ft.Container(
        image=ft.DecorationImage(
            src=background_image,
            fit=ft.ImageFit.COVER,
        ),
        margin=-10,
        alignment=ft.alignment.center,
        expand=True,
        content=content,
    )

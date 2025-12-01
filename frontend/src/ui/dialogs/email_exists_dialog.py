"""Email already exists dialog."""
import flet as ft
from typing import Callable, Optional


def show_email_exists_dialog(
        page: ft.Page,
        email: str,
        on_close: Optional[Callable] = None,
) -> None:
    """Display email already exists error dialog.

    Args:
        page: Flet page instance
        email: The email that already exists
        on_close: Callback when dialog is closed
    """

    def handle_ok(e):
        """Handle OK button click."""
        page.close(dialog)
        if on_close:
            on_close()

    # Build dialog
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(
                    name=ft.Icons.ERROR_OUTLINE_ROUNDED,
                    color=ft.Colors.ORANGE_700,
                    size=30,
                ),
                ft.Text(
                    "Organization Already Exists",
                    size=20,
                    weight=ft.FontWeight.W_700,
                    color=ft.Colors.ORANGE_900,
                ),
            ],
            spacing=10,
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f"An organization with the primary email",
                        size=15,
                        weight=ft.FontWeight.W_400,
                        color=ft.Colors.GREY_800,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        content=ft.Text(
                            email,
                            size=15,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.INDIGO_700,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        bgcolor=ft.Colors.GREY_100,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=50,
                        padding=ft.padding.only(left=10, right=10, top=5, bottom=5),
                    ),
                    ft.Text(
                        "already exists in our system.",
                        size=15,
                        weight=ft.FontWeight.W_400,
                        color=ft.Colors.GREY_800,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(height=20),
                    ft.Text(
                        "Please choose one of the following options:",
                        size=14,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(
                                            name=ft.Icons.MAIL_OUTLINE,
                                            size=20,
                                            color=ft.Colors.INDIGO_600,
                                        ),
                                        ft.Text(
                                            "Create organization with a different email",
                                            size=14,
                                            weight=ft.FontWeight.W_400,
                                            color=ft.Colors.GREY_800,
                                        ),
                                    ],
                                    spacing=10,
                                    expand=True,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                ft.Row(
                                    [
                                        ft.Icon(
                                            name=ft.Icons.CLOUD_SYNC_OUTLINED,
                                            size=20,
                                            color=ft.Colors.INDIGO_600,
                                        ),
                                        ft.Text(
                                            "Try connecting to existing organization",
                                            size=14,
                                            weight=ft.FontWeight.W_400,
                                            color=ft.Colors.GREY_800,
                                        ),
                                    ],
                                    expand=True,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=10,
                                ),
                            ],
                            spacing=12,
                        ),
                        padding=ft.padding.only(top=10, left=20),
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5,
            ),
            height=200,
            width=450,
        ),
        actions=[
            ft.TextButton(
                text="OK, Go Back",
                on_click=handle_ok,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    # Show dialog
    page.open(dialog)

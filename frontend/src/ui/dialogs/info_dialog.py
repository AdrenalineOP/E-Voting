"""Information dialog for admin account setup."""
import flet as ft


def show_info_dialog(page: ft.Page) -> None:
    """Display admin account information dialog.

    Args:
        page: Flet page instance
    """
    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(
                    name=ft.Icons.INFO_ROUNDED,
                    size=28,
                    color=ft.Colors.BLUE,
                ),
                ft.Text(
                    value="Important Information",
                    weight=ft.FontWeight.W_600,
                    size=18,
                ),
            ],
            spacing=10,
        ),
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        value=(
                            "This email will be the primary email for this organization. "
                            "Without this email you will not be able to sign in to this organization again. "
                            "Please ensure you provide a valid and accessible email address."
                        ),
                        size=14,
                        weight=ft.FontWeight.W_400,
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Text(
                        value=(
                            "If you ever wish to change the primary email, you can do so later from the Settings. "
                            "All OTPs and verification codes for this organization will be sent to this primary email."
                        ),
                        size=14,
                        weight=ft.FontWeight.W_400,
                    ),
                    ft.Divider(height=10, color="transparent"),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    name=ft.Icons.WARNING_AMBER_ROUNDED,
                                    size=20,
                                    color=ft.Colors.AMBER,
                                ),
                                ft.Text(
                                    value='Note: "Ensure your email remains confidential and accessible."',
                                    size=13,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.AMBER_900,
                                ),
                            ],
                            spacing=8,
                        ),
                        bgcolor=ft.Colors.AMBER_50,
                        border=ft.border.all(1, ft.Colors.AMBER_200),
                        border_radius=8,
                        padding=10,
                    ),
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            width=580,
            height=240,
        ),
        actions=[
            ft.TextButton(
                text="Got it!",
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        weight=ft.FontWeight.W_400,
                    ),
                ),
                on_click=lambda e: page.close(dialog),
                autofocus=True
            )
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.open(dialog)


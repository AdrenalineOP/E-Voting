"""Exit confirmation dialog."""
import flet as ft
from core.storage import ClientStorage
from core.storage_keys import StorageKey


def show_exit_dialog(page: ft.Page, storage: ClientStorage) -> None:
    """Display exit confirmation dialog.

    Args:
        page: Flet page instance
        storage: ClientStorage instance
    """
    checkbox = ft.Checkbox(
        label="Don't ask again",
        label_style=ft.TextStyle(weight=ft.FontWeight.W_400),
        value=False,
    )

    def handle_exit(e):
        """Exit application and save preference."""
        if checkbox.value:
            storage.set(StorageKey.PREVENT_CLOSE_DIALOG, False)
        page.window.destroy()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(name=ft.Icons.QUESTION_MARK_ROUNDED),
                ft.Text(
                    value="Confirm Exit",
                    weight=ft.FontWeight.W_500,
                ),
            ],
            spacing=10,
        ),
        content=ft.Column(
            [
                ft.Row([
                    ft.Row(width=1),
                    ft.Text(
                        value="Are you sure you want to exit?",
                        weight=ft.FontWeight.W_400,

                    )
                ]),
                checkbox,
            ],
            spacing=10,
            width=330,
            height=60,
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        weight=ft.FontWeight.W_400
                    )
                ),
                on_click=lambda e: page.close(dialog)
            ),
            ft.TextButton(
                text="Exit",
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        weight=ft.FontWeight.W_400
                    )
                ),
                on_click=handle_exit,
                autofocus=True
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.open(dialog)

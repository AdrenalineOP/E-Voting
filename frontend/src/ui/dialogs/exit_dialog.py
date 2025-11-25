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
        value=False,
    )

    def handle_cancel(e):
        """Close dialog without exiting."""
        dialog.open = False
        page.update()

    def handle_exit(e):
        """Exit application and save preference."""
        if checkbox.value:
            # User doesn't want to see this dialog again
            storage.set(StorageKey.PREVENT_CLOSE_DIALOG, False)
        page.window.destroy()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Row(
            [
                ft.Icon(name=ft.Icons.QUESTION_MARK_ROUNDED),
                ft.Text("Confirm Exit"),
            ],
            spacing=10,
        ),
        content=ft.Column(
            [
                ft.Text("Are you sure you want to exit?"),
                checkbox,
            ],
            tight=True,
            spacing=10,
        ),
        actions=[
            ft.TextButton("Cancel", on_click=handle_cancel),
            ft.TextButton("Exit", on_click=handle_exit, autofocus=True),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.dialog = dialog
    dialog.open = True
    page.update()

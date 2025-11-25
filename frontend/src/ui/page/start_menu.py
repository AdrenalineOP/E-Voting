"""Start menu page with improved organization."""
import flet as ft
from typing import Optional

from core import ClientStorage


class StartMenuPage:
    """Start menu page manager."""

    # Animation constants
    EXPANDED_IMAGE_HEIGHT = 370
    COLLAPSED_IMAGE_HEIGHT = 170
    ANIMATION_DURATION = 600

    def __init__(self, page: ft.Page, content_image: ft.Container, content_column: ft.Column, storage: ClientStorage):
        """Initialize start menu page.

        Args:
            page: Flet page instance
            content_image: Content image container
            content_column: Content column for menu items
            storage: Storage manager
        """
        self.page = page
        self.content_image = content_image
        self.content_column = content_column
        self.storage = storage
        self.settings_button: Optional[ft.FloatingActionButton] = None

    async def render_async(self) -> None:
        """Async render method for async contexts."""
        # Create and add settings button
        self.settings_button = ft.FloatingActionButton(
            icon=ft.Icons.CLOUD_SYNC_ROUNDED,
            tooltip="Manage Organization",
            on_click=self._on_settings_click,
        )

        if not self.storage.is_first_launch:
            self.page.floating_action_button = self.settings_button

        # Create menu buttons based on first launch status
        is_first = await self.storage.is_first_launch_async()
        menu_buttons = (
            self._create_first_launch_menu()
            if is_first
            else self._create_returning_user_menu()
        )

        # Set content
        self.content_column.controls = [
            ft.Column(
                controls=menu_buttons,
                width=250,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]

        self.page.update()

    def render(self) -> None:
        """Render the start menu page."""
        # Create and add settings button
        self.settings_button = ft.FloatingActionButton(
            icon=ft.Icons.CLOUD_SYNC_ROUNDED,
            tooltip="Manage Organization",
            on_click=self._on_settings_click,
        )
        if not self.storage.is_first_launch:
            self.page.floating_action_button = self.settings_button

        # Create menu buttons based on first launch status
        menu_buttons = (
            self._create_first_launch_menu()
            if self.storage.is_first_launch()
            else self._create_returning_user_menu()
        )

        # Set content
        self.content_column.controls = [
            ft.Column(
                controls=menu_buttons,
                width=250,
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]

        self.page.update()

    def _create_first_launch_menu(self) -> list[ft.Control]:
        """Create menu buttons for first launch.

        Returns:
            List of menu buttons
        """
        return [
            ft.ElevatedButton(
                text="Create Account",
                icon=ft.Icons.PERSON_ADD,
                height=50,
                width=250,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        weight=ft.FontWeight.W_400
                    )
                ),
                on_click=self._on_create_account,
            ),
            ft.ElevatedButton(
                text="Connect to Server",
                icon=ft.Icons.CLOUD_UPLOAD,
                height=50,
                width=250,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        weight=ft.FontWeight.W_400
                    )
                ),
                on_click=self._on_connect_server,
            )
        ]

    def _create_returning_user_menu(self) -> list[ft.Control]:
        """Create menu buttons for returning users.

        Returns:
            List of menu buttons
        """
        return [
            ft.ElevatedButton(
                text="Sign In",
                icon=ft.Icons.LOGIN,
                height=50,
                width=250,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        weight=ft.FontWeight.W_400
                    )
                ),
                on_click=self._on_sign_in,
            ),
            ft.ElevatedButton(
                text="Vote",
                icon=ft.Icons.HOW_TO_VOTE,
                height=50,
                width=250,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        weight=ft.FontWeight.W_400
                    )
                ),
                on_click=self._on_vote
            )
        ]

    def _animate_transition(self, image_height: int) -> None:
        """Animate page transition.

        Args:
            image_height: Target image height
        """
        self.content_image.height = image_height
        self.content_column.clean()
        self.page.update()

    def _prepare_navigation(self) -> None:
        """Prepare page for navigation (remove FAB, animate)."""
        if self.settings_button:
            self.page.floating_action_button = None
        self._animate_transition(self.COLLAPSED_IMAGE_HEIGHT)

    # Event handlers
    def _on_create_account(self, e: ft.ControlEvent) -> None:
        """Handle create account button click."""
        self._prepare_navigation()
        from .create_account import CreateAccountPage
        account_page = CreateAccountPage(
            self.page,
            self.content_image,
            self.content_column,
            self.storage
        )
        account_page.render()

    def _on_sign_in(self, e: ft.ControlEvent) -> None:
        """Handle sign in button click."""
        self._prepare_navigation()
        # TODO: Navigate to login page
        print("Navigate to: Sign In")

    def _on_connect_server(self, e: ft.ControlEvent) -> None:
        """Handle connect server button click."""
        self._prepare_navigation()
        # TODO: Navigate to server connection page
        print("Navigate to: Connect Server")

    def _on_vote(self, e: ft.ControlEvent) -> None:
        """Handle vote button click."""
        self._prepare_navigation()
        # TODO: Navigate to vote page
        print("Navigate to: Vote")

    def _on_settings_click(self, e: ft.ControlEvent) -> None:
        """Handle settings button click."""
        # TODO: Show settings dialog
        print("Open Settings Dialog")

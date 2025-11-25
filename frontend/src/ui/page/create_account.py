"""Create account page with organization and sign-up forms."""
import re
import asyncio
import flet as ft
from typing import Optional
from ui.dialogs import show_info_dialog, show_otp_dialog
from core import ClientStorage, StorageKey


class CreateAccountPage:
    """Create account page manager with multi-step form."""

    # Email validation regex
    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Animation constants
    EXPANDED_IMAGE_HEIGHT = 170
    COLLAPSED_IMAGE_HEIGHT = 0

    def __init__(
        self,
        page: ft.Page,
        content_image: ft.Container,
        content_column: ft.Column,
        storage: ClientStorage,
    ):
        """Initialize create account page.

        Args:
            page: Flet page instance
            content_image: Content image container
            content_column: Content column for forms
            storage: Storage manager
        """
        self.page = page
        self.content_image = content_image
        self.content_column = content_column
        self.storage = storage

        # Form data
        self.organization_name: Optional[str] = None
        self.election_name: Optional[str] = None

    def render(self) -> None:
        """Render the organization details form (step 1)."""
        self._render_organization_form()

    # ========== STEP 1: Organization Details ==========

    def _render_organization_form(self) -> None:
        """Render organization and election name input form."""
        # Input fields
        self.organization_entry = ft.TextField(
            hint_text="Enter your organization name",
            width=330,
            capitalization=ft.TextCapitalization.CHARACTERS,
            filled=False,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.BLACK,
            autofocus=True,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            error_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            on_change=self._validate_organization,
            on_submit=self._on_next_click,
        )

        self.election_entry = ft.TextField(
            hint_text="Enter your election name",
            width=330,
            capitalization=ft.TextCapitalization.CHARACTERS,
            filled=False,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.BLACK,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            error_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            on_change=self._validate_election,
            on_submit=self._on_next_click,
        )

        # Pre-fill if returning from next page
        if self.organization_name:
            self.organization_entry.value = self.organization_name
            self.election_entry.value = self.election_name

        # Next button
        self.next_button = ft.ElevatedButton(
            text="Next",
            height=50,
            width=340,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(weight=ft.FontWeight.W_400)
            ),
            on_click=self._on_next_click,
        )

        # Render content
        self.content_column.controls = [
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Setup Organization",
                                size=30,
                                color='#0c4a6e',
                                weight=ft.FontWeight.W_800,
                            ),
                        ],
                        width=450,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            self.organization_entry,
                            self.election_entry,
                            self.next_button,
                        ],
                        width=450,
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=30,
                    ),
                ],
                width=450,
                height=317,
                spacing=20,
            ),
            ft.Container(
                content=ft.Row(
                    [
                        ft.TextButton(
                            text="Back",
                            icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(weight=ft.FontWeight.W_400)
                            ),
                            on_click=self._on_back_to_menu,
                        ),
                    ],
                    width=450,
                ),
                bgcolor="#44CCCCCC",
                blur=ft.Blur(50, 50, ft.BlurTileMode.MIRROR),
                border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
            ),
        ]

        self.page.update()

    def _validate_organization(self, e: ft.ControlEvent) -> None:
        """Validate organization name input."""
        if self.organization_entry.value.strip():
            self.organization_entry.suffix_icon = None
            self.organization_entry.error_text = None
        else:
            self.organization_entry.error_text = "Please enter your organization name"
            self.organization_entry.suffix_icon = ft.Icons.ERROR_OUTLINE_ROUNDED
        self.organization_entry.update()

    def _validate_election(self, e: ft.ControlEvent) -> None:
        """Validate election name input."""
        if self.election_entry.value.strip():
            self.election_entry.suffix_icon = None
            self.election_entry.error_text = None
        else:
            self.election_entry.error_text = "Please enter the election name"
            self.election_entry.suffix_icon = ft.Icons.ERROR_OUTLINE_ROUNDED
        self.election_entry.update()

    async def _on_next_click(self, e: ft.ControlEvent) -> None:
        """Handle next button click."""
        # Validate both fields
        self._validate_organization(e)
        self._validate_election(e)

        if not self.organization_entry.value.strip():
            self.organization_entry.focus()
            return

        if not self.election_entry.value.strip():
            self.election_entry.focus()
            return

        # Show loading state
        self._set_loading_state(
            self.next_button,
            [self.organization_entry, self.election_entry],
            True,
        )

        # Save data
        self.organization_name = self.organization_entry.value
        self.election_name = self.election_entry.value

        # Animate and transition
        self.content_image.height = self.COLLAPSED_IMAGE_HEIGHT
        self.content_image.update()

        await asyncio.sleep(0.2)

        self.content_column.clean()
        self.page.update()

        # Go to sign-up form
        self._render_signup_form()

    # ========== STEP 2: Sign Up Form ==========

    def _render_signup_form(self) -> None:
        """Render admin sign-up form (step 2)."""
        # Input fields
        self.username_entry = ft.TextField(
            hint_text="Enter your username",
            width=330,
            prefix_icon=ft.Icons.PERSON_ROUNDED,
            filled=False,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.BLACK,
            autofocus=True,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            error_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            on_change=self._validate_username,
            on_submit=lambda e: self.email_entry.focus(),
        )

        self.email_entry = ft.TextField(
            hint_text="Enter your email address",
            width=330,
            prefix_icon=ft.Icons.MAIL_ROUNDED,
            filled=False,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.BLACK,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            error_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            on_change=self._validate_email,
            on_submit=lambda e: self.password_entry.focus(),
        )

        self.password_entry = ft.TextField(
            hint_text="Enter your password",
            width=330,
            prefix_icon=ft.Icons.LOCK_OPEN_ROUNDED,
            filled=False,
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.BLACK,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            error_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            on_change=self._validate_password,
            on_submit=lambda e: self.confirm_password_entry.focus(),
        )

        self.confirm_password_entry = ft.TextField(
            hint_text="Confirm your password",
            width=330,
            prefix_icon=ft.Icons.LOCK_ROUNDED,
            filled=False,
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.BLACK,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            error_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            on_change=self._validate_confirm_password,
            on_submit=self._on_signup_click,
        )

        # Sign up button
        self.signup_button = ft.ElevatedButton(
            text="Create Account",
            height=50,
            width=340,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(weight=ft.FontWeight.W_400)
            ),
            on_click=self._on_signup_click,
        )

        # Render content
        self.content_column.controls = [
            ft.Row(height=10),
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                value="Create Admin Account",
                                size=30,
                                color='#0c4a6e',
                                weight=ft.FontWeight.W_800,
                            ),
                        ],
                        width=450,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            self.username_entry,
                            self.email_entry,
                            self.password_entry,
                            self.confirm_password_entry,  # NEW
                            self.signup_button,
                        ],
                        width=450,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=35,
                    ),
                ],
                width=450,
                height=457,
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
            ft.Container(
                content=ft.Row(
                    [
                        ft.TextButton(
                            text="Back",
                            icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(weight=ft.FontWeight.W_400)
                            ),
                            on_click=self._on_back_to_organization,
                        ),
                        ft.TextButton(
                            text="Important!",
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(
                                    weight=ft.FontWeight.W_400,
                                    color=ft.Colors.RED_300,
                                )
                            ),
                            on_click=lambda e: show_info_dialog(self.page),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=450,
                ),
                bgcolor='#44CCCCCC',
                blur=ft.Blur(50, 50, ft.BlurTileMode.MIRROR),
                border_radius=ft.border_radius.only(bottom_left=15, bottom_right=15)
            ),
        ]

        self.page.update()

    def _validate_username(self, e: ft.ControlEvent) -> None:
        """Validate username input."""
        if self.username_entry.value.strip():
            self.username_entry.suffix_icon = None
            self.username_entry.error_text = None
        else:
            self.username_entry.error_text = "Please enter a username"
            self.username_entry.suffix_icon = ft.Icons.ERROR_OUTLINE_ROUNDED
        self.username_entry.update()

    def _validate_email(self, e: ft.ControlEvent) -> None:
        """Validate email input."""
        email = self.email_entry.value.strip()

        if not email:
            self.email_entry.error_text = "Please enter your email address"
            self.email_entry.suffix_icon = ft.Icons.ERROR_OUTLINE_ROUNDED
        elif re.fullmatch(self.EMAIL_REGEX, email):
            self.email_entry.suffix_icon = ft.Icons.CHECK_CIRCLE
            self.email_entry.error_text = None
        else:
            self.email_entry.error_text = "Please enter a valid email address"
            self.email_entry.suffix_icon = ft.Icons.CLOSE_ROUNDED

        self.email_entry.update()

    def _validate_password(self, e: ft.ControlEvent) -> None:
        """Validate password input."""
        password = self.password_entry.value

        if not password:
            self.password_entry.error_text = "Please enter a password"
        elif len(password) < 8:
            self.password_entry.error_text = "Password must be at least 8 characters long"
        else:
            self.password_entry.error_text = None

        self.password_entry.update()

    def _validate_confirm_password(self, e: ft.ControlEvent) -> None:
        """Validate confirm password matches password."""
        confirm_password = self.confirm_password_entry.value
        password = self.password_entry.value

        if not confirm_password:
            self.confirm_password_entry.error_text = "Please confirm your password"
            self.confirm_password_entry.suffix_icon = ft.Icons.ERROR_OUTLINE_ROUNDED
        elif confirm_password != password:
            self.confirm_password_entry.error_text = "Passwords do not match"
            self.confirm_password_entry.suffix_icon = ft.Icons.CLOSE_ROUNDED
        else:
            self.confirm_password_entry.error_text = None
            self.confirm_password_entry.suffix_icon = ft.Icons.CHECK_CIRCLE

        self.confirm_password_entry.update()

    async def _on_signup_click(self, e: ft.ControlEvent) -> None:
        """Handle sign-up button click."""
        # Validate all fields
        self._validate_username(e)
        self._validate_email(e)
        self._validate_password(e)
        self._validate_confirm_password(e)  # NEW

        # Check all validations passed
        if not self._all_signup_fields_valid():
            return

        # Show loading state
        self._set_loading_state(
            self.signup_button,
            [self.username_entry, self.email_entry, self.password_entry, self.confirm_password_entry],  # NEW
            True,
        )

        await asyncio.sleep(0.3)

        # Reset button for OTP dialog
        self._set_loading_state(
            self.signup_button,
            [self.username_entry, self.email_entry, self.password_entry, self.confirm_password_entry],  # NEW
            False,
        )

        # Show OTP dialog
        def verify_otp(otp_code: str) -> bool:
            """Verify OTP code - accepts any 5 digits for now."""
            return len(otp_code) == 5 and otp_code.isdigit()

        def on_otp_success():
            """Handle successful OTP verification."""
            # Save to storage
            self.storage.set(StorageKey.ORGANIZATION_ID, f"ORG-{self.organization_name}")
            self.storage.set(StorageKey.SYSTEM_ID, "SYS-001")

            # Navigate to all done page
            self.content_column.clean()
            self.page.update()

            from .all_done import AllDonePage
            done_page = AllDonePage(self.page, self.content_column, self.storage)
            done_page.render()

        show_otp_dialog(
            page=self.page,
            email=self.email_entry.value,
            on_verify=verify_otp,
            on_success=on_otp_success,
        )

    def _all_signup_fields_valid(self) -> bool:
        """Check if all signup fields are valid."""
        username_valid = bool(self.username_entry.value.strip())
        email_valid = bool(
            self.email_entry.value.strip() and
            re.fullmatch(self.EMAIL_REGEX, self.email_entry.value)
        )
        password_valid = len(self.password_entry.value) >= 8
        confirm_password_valid = (
                self.confirm_password_entry.value == self.password_entry.value and
                len(self.confirm_password_entry.value) >= 8
        )

        return username_valid and email_valid and password_valid and confirm_password_valid

    # ========== Navigation Handlers ==========

    async def _on_back_to_menu(self, e: ft.ControlEvent) -> None:
        """Navigate back to start menu."""
        self.organization_name = None
        self.election_name = None

        self.content_image.height = 370
        self.content_image.update()
        await asyncio.sleep(0.2)

        self.content_column.clean()
        self.page.update()

        # Import and render start menu
        from .start_menu import StartMenuPage
        menu = StartMenuPage(self.page, self.content_image, self.content_column, self.storage)
        await menu.render_async()

    async def _on_back_to_organization(self, e: ft.ControlEvent) -> None:
        """Navigate back to organization form."""
        self.content_image.height = self.EXPANDED_IMAGE_HEIGHT
        self.content_image.update()
        await asyncio.sleep(0.4)

        self.content_column.clean()
        self.page.update()

        self._render_organization_form()

    # ========== UI Helper Methods ==========

    def _set_loading_state(
        self,
        button: ft.ElevatedButton,
        fields: list[ft.TextField],
        loading: bool,
    ) -> None:
        """Set loading state for button and disable/enable fields."""
        if loading:
            button.content = ft.ProgressRing(height=25, width=25, stroke_width=3)
            button.text = None
            button.disabled = True
            button.opacity = 0.5
            for field in fields:
                field.disabled = True
        else:
            button.content = None
            button.text = "Create Account" if "Account" in str(button.data or "Create Account") else "Next"
            button.disabled = False
            button.opacity = 1
            for field in fields:
                field.disabled = False

        self.page.update()

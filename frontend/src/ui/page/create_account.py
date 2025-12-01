"""Create account page with organization and sign-up forms."""
import re
import asyncio
import flet as ft
from typing import Optional
from ui.dialogs import show_info_dialog, show_otp_dialog, show_email_exists_dialog
from core import (
    ClientStorage,
    StorageKey,
    API,
    generate_org_code,
    NetworkError,
    APIException,
    ValidationError,
    EmailAlreadyExistsError,
)


class CreateAccountPage:
    """Create account page manager with multi-step form."""

    # Email validation regex
    EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    # Animation constants
    EXPANDED_IMAGE_HEIGHT = 170
    COLLAPSED_IMAGE_HEIGHT = 0

    # API timeout (15 seconds)
    API_TIMEOUT = 15

    def __init__(
            self,
            page: ft.Page,
            content_image: ft.Container,
            content_column: ft.Column,
            storage: ClientStorage,
            api: API,
    ):
        """Initialize create account page."""
        self.page = page
        self.content_image = content_image
        self.content_column = content_column
        self.storage = storage
        self.api = api

        # Form data
        self.organization_name: Optional[str] = None
        self.election_name: Optional[str] = None

        # UI References for signup page
        self.back_button: Optional[ft.TextButton] = None
        self.important_button: Optional[ft.TextButton] = None

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
            on_submit=self._on_signup_click,
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
            on_submit=self._on_signup_click,
        )

        self.password_entry = ft.TextField(
            hint_text="Enter your password",
            width=330,
            prefix_icon=ft.Icons.LOCK_ROUNDED,
            filled=False,
            password=True,
            can_reveal_password=True,
            border=ft.InputBorder.UNDERLINE,
            border_color=ft.Colors.BLACK,
            text_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            error_style=ft.TextStyle(weight=ft.FontWeight.W_400),
            on_change=self._validate_password,
            on_submit=self._on_signup_click,
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

        # Bottom action buttons (store references)
        self.back_button = ft.TextButton(
            text="Back",
            icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(weight=ft.FontWeight.W_400)
            ),
            on_click=self._on_back_to_organization,
        )

        self.important_button = ft.TextButton(
            text="Important!",
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(
                    weight=ft.FontWeight.W_400,
                    color=ft.Colors.RED_300,
                )
            ),
            on_click=lambda e: show_info_dialog(self.page),
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
                            self.confirm_password_entry,
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
                        self.back_button,
                        self.important_button,
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
        elif confirm_password != password:
            self.confirm_password_entry.error_text = "Passwords do not match"
        else:
            self.confirm_password_entry.error_text = None

        self.confirm_password_entry.update()

    async def _on_signup_click(self, e: ft.ControlEvent) -> None:
        """Handle sign-up button click."""
        # Validate all fields
        self._validate_username(e)
        self._validate_email(e)
        self._validate_password(e)
        self._validate_confirm_password(e)

        # Check all validations passed
        if not self.username_entry.value.strip():
            self.username_entry.focus()
            return

        if not self.email_entry.value.strip():
            self.email_entry.focus()
            return

        if not self.password_entry.value.strip():
            self.password_entry.focus()
            return

        if not self.confirm_password_entry.value.strip():
            self.confirm_password_entry.focus()
            return

        if self.password_entry.value != self.confirm_password_entry.value:
            self.confirm_password_entry.focus()
            return

        # Show loading state AND disable Back/Important buttons
        self._set_signup_loading_state(True)

        try:
            # STEP 1: Send OTP to email
            otp_response = self.api.otp.send_otp(
                email=self.email_entry.value,
                name=self.username_entry.value,
            )

            # Store current session token
            current_session_token = otp_response.get("session_token")
            expires_in = otp_response.get("expires_in_minutes", 5)

            # Reset loading for OTP dialog
            self._set_signup_loading_state(False)

            # Resend OTP handler
            def resend_otp() -> dict:
                """Resend OTP - generates new session token."""
                nonlocal current_session_token

                try:
                    # Call backend to send new OTP (cleans old one automatically)
                    new_response = self.api.otp.send_otp(
                        email=self.email_entry.value,
                        name=self.username_entry.value,
                    )

                    # Update session token with new one
                    current_session_token = new_response.get("session_token")

                    return new_response

                except Exception as e:
                    raise e

            # Verify OTP handler
            def verify_otp_with_backend(otp_code: str) -> bool:
                """Verify OTP with backend - uses current session token."""
                try:
                    # Call backend to verify OTP using current session token
                    verify_response = self.api.otp.verify_otp(
                        session_token=current_session_token,
                        otp=otp_code,
                    )
                    return verify_response.get("success", False)
                except Exception:
                    return False

            async def on_otp_success():
                """Handle successful OTP verification and create organization."""
                # Re-enable loading after OTP verified
                self._set_signup_loading_state(True)

                try:
                    # Generate random 8-character organization code
                    org_code = generate_org_code(8)

                    # Show progress
                    self.page.open(
                        ft.SnackBar(
                            content=ft.Text("Creating organization..."),
                            bgcolor=ft.Colors.BLUE,
                        )
                    )

                    # Create task with timeout
                    create_task = asyncio.create_task(
                        self._create_organization_request(org_code)
                    )

                    # Wait with timeout (15 seconds)
                    try:
                        response = await asyncio.wait_for(create_task, timeout=self.API_TIMEOUT)

                        # Save organization data to storage
                        await self.storage.set_async(StorageKey.ORGANIZATION_ID, response.get("org_id"))
                        await self.storage.set_async(StorageKey.ORGANIZATION_CODE, response.get("code"))
                        await self.storage.set_async(StorageKey.PRIMARY_EMAIL, response.get("primary_email"))

                        # Show success message
                        self.page.open(
                            ft.SnackBar(
                                content=ft.Text("✓ Organization created successfully!"),
                                bgcolor=ft.Colors.GREEN,
                            )
                        )

                        await asyncio.sleep(1)

                        # Navigate to all done page
                        self.content_column.clean()
                        self.page.update()

                        from .all_done import AllDonePage
                        done_page = AllDonePage(self.page, self.content_column, self.storage)
                        done_page.render()

                    except asyncio.TimeoutError:
                        self.page.open(
                            ft.SnackBar(
                                content=ft.Text("❌ Something went wrong. Try again."),
                                bgcolor=ft.Colors.RED,
                                duration=5000,
                            )
                        )
                        self._set_signup_loading_state(False)

                except EmailAlreadyExistsError:
                    self._set_signup_loading_state(False)

                    async def on_dialog_close():
                        """Navigate back to start menu after dialog closes."""
                        self.organization_name = None
                        self.election_name = None

                        self.content_image.height = 370
                        self.content_image.update()
                        await asyncio.sleep(0.2)

                        self.content_column.clean()
                        self.page.update()

                        from .start_menu import StartMenuPage
                        menu = StartMenuPage(self.page, self.content_image, self.content_column, self.storage, self.api)
                        await menu.render_async()

                    show_email_exists_dialog(
                        page=self.page,
                        email=self.email_entry.value,
                        on_close=lambda: asyncio.create_task(on_dialog_close()),
                    )

                except (NetworkError, ValidationError, APIException):
                    self.page.open(
                        ft.SnackBar(
                            content=ft.Text("❌ Something went wrong. Try again."),
                            bgcolor=ft.Colors.RED,
                            duration=5000,
                        )
                    )
                    self._set_signup_loading_state(False)

                except Exception:
                    self.page.open(
                        ft.SnackBar(
                            content=ft.Text("❌ Something went wrong. Try again."),
                            bgcolor=ft.Colors.RED,
                            duration=5000,
                        )
                    )
                    self._set_signup_loading_state(False)

            def on_otp_cancel():
                """Handle OTP dialog cancellation."""
                pass

            # Show OTP dialog with resend functionality
            show_otp_dialog(
                page=self.page,
                email=self.email_entry.value,
                username=self.username_entry.value,
                expires_in_minutes=expires_in,
                on_verify=verify_otp_with_backend,
                on_resend=resend_otp,  # NEW: Resend handler
                on_success=on_otp_success,
                on_cancel=on_otp_cancel,
            )

        except (NetworkError, APIException):
            self.page.open(
                ft.SnackBar(
                    content=ft.Text("❌ Failed to send OTP. Check your connection."),
                    bgcolor=ft.Colors.RED,
                    duration=5000,
                )
            )
            self._set_signup_loading_state(False)

        except Exception:
            self.page.open(
                ft.SnackBar(
                    content=ft.Text("❌ Something went wrong. Try again."),
                    bgcolor=ft.Colors.RED,
                    duration=5000,
                )
            )
            self._set_signup_loading_state(False)

    async def _create_organization_request(self, org_code: str) -> dict:
        """Make the API request to create organization.
        
        Args:
            org_code: Generated organization code
            
        Returns:
            Response data from API
        """
        return self.api.organizations.create_organization(
            name=self.organization_name,
            code=org_code,
            primary_email=self.email_entry.value,
        )

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
        menu = StartMenuPage(self.page, self.content_image, self.content_column, self.storage, self.api)
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
            button.text = "Next"
            button.disabled = False
            button.opacity = 1
            for field in fields:
                field.disabled = False

        self.page.update()

    def _set_signup_loading_state(self, loading: bool) -> None:
        """Set loading state for signup button, fields, and action buttons.
        
        Args:
            loading: True to show loading, False to reset
        """
        if loading:
            # Button loading
            self.signup_button.content = ft.ProgressRing(height=25, width=25, stroke_width=3)
            self.signup_button.text = None
            self.signup_button.disabled = True
            self.signup_button.opacity = 0.5

            # Disable all input fields
            self.username_entry.disabled = True
            self.email_entry.disabled = True
            self.password_entry.disabled = True
            self.confirm_password_entry.disabled = True

            # Disable Back and Important buttons
            if self.back_button:
                self.back_button.disabled = True
                self.back_button.opacity = 0.3
            if self.important_button:
                self.important_button.disabled = True
                self.important_button.opacity = 0.3
        else:
            # Reset button
            self.signup_button.content = None
            self.signup_button.text = "Create Account"
            self.signup_button.disabled = False
            self.signup_button.opacity = 1

            # Enable all input fields
            self.username_entry.disabled = False
            self.email_entry.disabled = False
            self.password_entry.disabled = False
            self.confirm_password_entry.disabled = False

            # Enable Back and Important buttons
            if self.back_button:
                self.back_button.disabled = False
                self.back_button.opacity = 1
            if self.important_button:
                self.important_button.disabled = False
                self.important_button.opacity = 1

        self.page.update()

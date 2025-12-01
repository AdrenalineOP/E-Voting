"""OTP verification dialog with modern UI and resend functionality."""
import flet as ft
import asyncio
from typing import Callable, Optional


def show_otp_dialog(
        page: ft.Page,
        email: str,
        username: str,
        on_verify: Callable[[str], bool],
        on_resend: Callable[[], dict],  # NEW: Returns new session data
        on_success: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        expires_in_minutes: int = 5,
) -> None:
    """Display OTP verification dialog with resend functionality.

    Args:
        page: Flet page instance
        email: Email address where OTP was sent
        username: User's name
        on_verify: Callback function to verify OTP (returns True if valid)
        on_resend: Callback to resend OTP (returns new session data)
        on_success: Callback when OTP is successfully verified
        on_cancel: Optional callback when user cancels
        expires_in_minutes: OTP expiry time in minutes (from backend)
    """

    # Timer countdown - 30 seconds for resend
    resend_countdown = 30

    # OTP input fields (5 digits)
    otp_fields = []
    for i in range(5):
        field = ft.TextField(
            width=60,
            height=70,
            text_align=ft.TextAlign.CENTER,
            text_size=24,
            max_length=1,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=ft.Colors.INDIGO_200,
            focused_border_color=ft.Colors.INDIGO_600,
            filled=True,
            bgcolor=ft.Colors.INDIGO_50,
            border_radius=10,
            text_style=ft.TextStyle(
                weight=ft.FontWeight.W_600,
            ),
        )
        otp_fields.append(field)

    # Auto-focus next field and handle backspace
    def on_otp_change(e, index):
        """Move to next field automatically or handle backspace."""
        if e.control.value and index < 4:
            # Forward: move to next field when typing
            otp_fields[index + 1].focus()
        elif not e.control.value and index > 0:
            # Backward: move to previous field on delete/backspace
            otp_fields[index - 1].focus()
        page.update()

    # Attach change handlers
    for i, field in enumerate(otp_fields):
        field.on_change = lambda e, idx=i: on_otp_change(e, idx)

    # Error text
    error_text = ft.Text(
        value="",
        color=ft.Colors.RED,
        size=13,
        weight=ft.FontWeight.W_500,
        visible=False,
    )

    # Verify button
    verify_button = ft.ElevatedButton(
        text="Verify Code",
        width=300,
        height=50,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.INDIGO_600,
            color=ft.Colors.WHITE,
            text_style=ft.TextStyle(
                weight=ft.FontWeight.W_600,
                size=16,
            ),
        ),
    )

    # Resend button with countdown
    resend_text = ft.Text(
        value=f"Resend Code in {resend_countdown}s",
        size=14,
        weight=ft.FontWeight.W_500,
        color=ft.Colors.GREY_500,
    )

    resend_button = ft.TextButton(
        text="",
        content=resend_text,
        disabled=True,
        style=ft.ButtonStyle(
            color=ft.Colors.INDIGO_700,
            text_style=ft.TextStyle(
                weight=ft.FontWeight.W_500,
            ),
        ),
    )

    # Countdown timer
    async def countdown_timer():
        """Handle resend countdown - 30 seconds."""
        nonlocal resend_countdown
        while resend_countdown > 0:
            await asyncio.sleep(1)
            resend_countdown -= 1
            resend_text.value = f"Resend Code in {resend_countdown}s"
            page.update()

        # Enable resend after countdown
        resend_text.value = "Resend Code"
        resend_text.color = ft.Colors.INDIGO_700
        resend_button.disabled = False
        page.update()

    async def handle_verify(e):
        """Handle OTP verification."""
        # Get OTP value
        otp = "".join([field.value or "" for field in otp_fields])

        if len(otp) != 5:
            error_text.value = "Please enter all 5 digits"
            error_text.visible = True
            page.update()
            return

        # Show loading
        verify_button.content = ft.ProgressRing(width=20, height=20, color=ft.Colors.WHITE, stroke_width=2)
        verify_button.text = None
        verify_button.disabled = True
        for field in otp_fields:
            field.disabled = True
        page.update()

        await asyncio.sleep(0.5)  # Simulate API call

        # Verify OTP
        try:
            is_valid = on_verify(otp)

            if is_valid:
                # Show success
                error_text.value = "✓ Verification successful!"
                error_text.color = ft.Colors.GREEN
                error_text.visible = True
                page.update()

                await asyncio.sleep(0.5)  # Brief pause to show success message

                # CLOSE DIALOG IMMEDIATELY - DON'T WAIT FOR on_success
                page.close(dialog)

                # Call success callback in background (non-blocking)
                if on_success:
                    if asyncio.iscoroutinefunction(on_success):
                        # Create task to run in background
                        asyncio.create_task(on_success())
                    else:
                        on_success()
            else:
                # Show error and reset
                error_text.value = "Invalid OTP code. Please try again."
                error_text.color = ft.Colors.RED
                error_text.visible = True

                verify_button.content = None
                verify_button.text = "Verify Code"
                verify_button.disabled = False

                for field in otp_fields:
                    field.value = ""
                    field.disabled = False

                otp_fields[0].focus()
                page.update()

        except Exception as e:
            # Handle any unexpected errors during verification
            error_text.value = "Server error. Please try again."
            error_text.color = ft.Colors.RED
            error_text.visible = True

            verify_button.content = None
            verify_button.text = "Verify Code"
            verify_button.disabled = False

            for field in otp_fields:
                field.disabled = False

            page.update()

    async def handle_resend(e):
        """Handle resend OTP - calls backend to generate new OTP."""
        nonlocal resend_countdown

        # Disable resend button and show loading
        resend_button.disabled = True
        resend_text.value = "Sending..."
        resend_text.color = ft.Colors.GREY_500
        page.update()

        try:
            # Call backend to resend OTP (generates new OTP, cleans old one)
            new_session_data = on_resend()

            # Show success
            resend_text.value = "✓ New code sent!"
            resend_text.color = ft.Colors.GREEN
            page.update()

            await asyncio.sleep(2)

            # Clear OTP fields
            for field in otp_fields:
                field.value = ""
            otp_fields[0].focus()
            page.update()

            # Restart countdown (30 seconds)
            resend_countdown = 30
            await countdown_timer()

        except Exception as e:
            # Show error
            resend_text.value = "Failed to send. Try again"
            resend_text.color = ft.Colors.RED
            page.update()

            await asyncio.sleep(2)

            # Re-enable resend button
            resend_text.value = "Resend Code"
            resend_text.color = ft.Colors.INDIGO_700
            resend_button.disabled = False
            page.update()

    async def handle_cancel(e):
        """Handle cancel button - ASYNC VERSION."""
        page.close(dialog)

        # Call cancel callback
        if on_cancel:
            if asyncio.iscoroutinefunction(on_cancel):
                await on_cancel()
            else:
                on_cancel()

    # Attach handlers
    verify_button.on_click = handle_verify
    resend_button.on_click = handle_resend

    # Build dialog
    dialog = ft.AlertDialog(
        modal=True,
        content=ft.Container(
            content=ft.Column(
                [
                    # OTP Image
                    ft.Container(
                        content=ft.Image(
                            src="/images/verification_img.png",
                            width=150,
                            height=150,
                            fit=ft.ImageFit.CONTAIN,
                        ),
                        alignment=ft.alignment.center,
                    ),
                    # Title
                    ft.Text(
                        value="Verify Your Email",
                        size=24,
                        weight=ft.FontWeight.W_700,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.INDIGO_900,
                    ),
                    # Description
                    ft.Text(
                        value=f"We've sent a verification code to\n{email}",
                        size=14,
                        weight=ft.FontWeight.W_400,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Divider(height=20, color="transparent"),
                    # OTP Input Fields
                    ft.Row(
                        controls=otp_fields,
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    # Error text
                    ft.Container(
                        content=error_text,
                        alignment=ft.alignment.center,
                        height=30,
                    ),
                    # Verify button
                    ft.Container(
                        content=verify_button,
                        alignment=ft.alignment.center,
                    ),
                    # Resend link with countdown
                    ft.Container(
                        content=resend_button,
                        alignment=ft.alignment.center,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                width=450,
            ),
            padding=30,
            border_radius=15,
            height=580,
        ),
        actions=[
            ft.TextButton(
                text="Cancel",
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        weight=ft.FontWeight.W_400,
                    ),
                ),
                on_click=handle_cancel,
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    # Show dialog and start countdown
    page.open(dialog)
    otp_fields[0].focus()

    # Start countdown timer (30 seconds)
    asyncio.create_task(countdown_timer())

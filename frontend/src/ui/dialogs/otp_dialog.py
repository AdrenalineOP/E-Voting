"""OTP verification dialog with modern UI."""
import flet as ft
import asyncio
from typing import Callable, Optional


def show_otp_dialog(
    page: ft.Page,
    email: str,
    on_verify: Callable[[str], bool],
    on_success: Optional[Callable] = None,
    on_cancel: Optional[Callable] = None,
) -> None:
    """Display OTP verification dialog with cool UI.

    Args:
        page: Flet page instance
        email: Email address where OTP was sent
        on_verify: Callback function to verify OTP (returns True if valid)
        on_success: Callback when OTP is successfully verified
        on_cancel: Optional callback when user cancels
    """

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
            border_color=ft.Colors.BLUE_200,
            focused_border_color=ft.Colors.BLUE,
            filled=True,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            text_style=ft.TextStyle(
                weight=ft.FontWeight.W_600,
            ),
        )
        otp_fields.append(field)

    # Auto-focus next field
    def on_otp_change(e, index):
        """Move to next field automatically."""
        if e.control.value and index < 4:
            otp_fields[index + 1].focus()

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
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            text_style=ft.TextStyle(
                weight=ft.FontWeight.W_600,
                size=16,
            ),
        ),
    )

    # Resend button
    resend_button = ft.TextButton(
        text="Resend Code",
        style=ft.ButtonStyle(
            color=ft.Colors.BLUE_700,
            text_style=ft.TextStyle(
                weight=ft.FontWeight.W_500,
            ),
        ),
    )

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
        verify_button.content = ft.ProgressRing(width=20, height=20, color=ft.Colors.WHITE)
        verify_button.text = None
        verify_button.disabled = True
        for field in otp_fields:
            field.disabled = True
        page.update()

        await asyncio.sleep(0.5)  # Simulate API call

        # Verify OTP
        is_valid = on_verify(otp)

        if is_valid:
            # Show success
            error_text.value = "✓ Verification successful!"
            error_text.color = ft.Colors.GREEN
            error_text.visible = True
            page.update()

            await asyncio.sleep(1)
            page.close(dialog)

            # Call success callback
            if on_success:
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

    async def handle_resend(e):
        """Handle resend OTP."""
        resend_button.text = "Code Sent! ✓"
        resend_button.disabled = True
        page.update()

        await asyncio.sleep(2)

        resend_button.text = "Resend Code"
        resend_button.disabled = False
        page.update()

    def handle_cancel(e):
        """Handle cancel button."""
        if on_cancel:
            on_cancel()
        page.close(dialog)

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

                    # Resend link
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

    page.open(dialog)
    otp_fields[0].focus()

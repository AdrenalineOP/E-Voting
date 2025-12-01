"""OTP API endpoints."""
from typing import Dict, Any
from .client import APIClient


class OTPAPI:
    """OTP endpoints."""

    def __init__(self, client: APIClient):
        self.client = client

    def send_otp(self, email: str, name: str) -> Dict[str, Any]:
        """Send OTP to email address.

        Args:
            email: Email address to send OTP to
            name: Recipient name

        Returns:
            Response with session_token and expiry info
            {
                "message": "OTP sent successfully to your email",
                "session_token": "abc123...",
                "expires_in_minutes": 5
            }
        """
        return self.client.post(
            "/otp/send",
            json={
                "email": email,
                "name": name,
            },
            include_auth=False,
        )

    def verify_otp(self, session_token: str, otp: str) -> Dict[str, Any]:
        """Verify OTP code.

        Args:
            session_token: Session token from send_otp response
            otp: OTP code entered by user

        Returns:
            Verification response
            {
                "success": true,
                "message": "OTP verified successfully",
                "email": "user@example.com"
            }
        """
        return self.client.post(
            "/otp/verify",
            json={
                "session_token": session_token,
                "otp": otp,
            },
            include_auth=False,
        )

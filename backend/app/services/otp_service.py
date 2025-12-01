import random
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
import uuid as uuid_pkg
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class OTPService:
    """
    OTP generation and verification service
    """

    def __init__(self):
        # In-memory storage for OTPs (use Redis in production)
        self.otp_storage: Dict[str, Dict] = {}
        self.otp_length = settings.OTP_LENGTH
        self.expiry_minutes = settings.OTP_EXPIRY_MINUTES

    def generate_otp(self) -> str:
        """
        Generate a random OTP

        Returns:
            str: Generated OTP
        """
        digits = string.digits
        otp = ''.join(random.choice(digits) for _ in range(self.otp_length))
        return otp

    def store_otp(self, email: str, otp: str) -> str:
        """
        Store OTP with expiry time

        Args:
            email: User's email address
            otp: Generated OTP

        Returns:
            str: Session token for OTP verification
        """
        session_token = str(uuid_pkg.uuid4())
        expiry_time = datetime.utcnow() + timedelta(minutes=self.expiry_minutes)

        self.otp_storage[session_token] = {
            "email": email,
            "otp": otp,
            "expiry": expiry_time,
            "attempts": 0
        }

        logger.info(f"OTP stored for email: {email}, expires at: {expiry_time}")
        return session_token

    def verify_otp(self, session_token: str, otp: str) -> Tuple[bool, str, Optional[str]]:
        """
        Verify OTP against stored value

        Args:
            session_token: Session token from store_otp
            otp: OTP to verify

        Returns:
            tuple: (is_valid, message, email)
        """
        # Check if session exists
        if session_token not in self.otp_storage:
            return False, "Invalid or expired session", None

        stored_data = self.otp_storage[session_token]

        # Check if OTP expired
        if datetime.utcnow() > stored_data["expiry"]:
            del self.otp_storage[session_token]
            return False, "OTP has expired", None

        # Check attempts (max 3 attempts)
        if stored_data["attempts"] >= 3:
            email = stored_data["email"]
            del self.otp_storage[session_token]
            return False, "Maximum verification attempts exceeded", email

        # Increment attempts
        stored_data["attempts"] += 1

        # Verify OTP
        if stored_data["otp"] == otp:
            email = stored_data["email"]
            del self.otp_storage[session_token]  # Remove after successful verification
            logger.info(f"OTP verified successfully for email: {email}")
            return True, "OTP verified successfully", email

        return False, "Invalid OTP", stored_data["email"]

    def get_email_from_token(self, session_token: str) -> Optional[str]:
        """
        Get email associated with session token

        Args:
            session_token: Session token

        Returns:
            Optional[str]: Email address or None
        """
        if session_token in self.otp_storage:
            return self.otp_storage[session_token]["email"]
        return None

    def cleanup_expired_otps(self):
        """
        Remove expired OTPs from storage
        """
        current_time = datetime.utcnow()
        expired_tokens = [
            token for token, data in self.otp_storage.items()
            if current_time > data["expiry"]
        ]

        for token in expired_tokens:
            del self.otp_storage[token]

        if expired_tokens:
            logger.info(f"Cleaned up {len(expired_tokens)} expired OTPs")


# Create singleton instance
otp_service = OTPService()

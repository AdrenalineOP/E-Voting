from pydantic import BaseModel, EmailStr
from typing import Optional

class OTPSendRequest(BaseModel):
    """Schema for sending OTP"""
    email: EmailStr
    name: str = "User"

class OTPSendResponse(BaseModel):
    """Schema for OTP send response"""
    message: str
    session_token: str
    expires_in_minutes: int

class OTPVerifyRequest(BaseModel):
    """Schema for verifying OTP"""
    session_token: str
    otp: str

class OTPVerifyResponse(BaseModel):
    """Schema for OTP verification response"""
    success: bool
    message: str
    email: Optional[str] = None  # Made optional with default None

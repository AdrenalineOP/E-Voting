from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from app.schemas.otp import (
    OTPSendRequest,
    OTPSendResponse,
    OTPVerifyRequest,
    OTPVerifyResponse
)
from app.services.otp_service import otp_service
from app.services.email_service import email_service
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/otp", tags=["OTP Authentication"])


@router.post("/send", response_model=OTPSendResponse)
async def send_otp(
        request: OTPSendRequest,
        background_tasks: BackgroundTasks
):
    """
    Send OTP to user's email address
    """
    try:
        # Generate OTP
        otp = otp_service.generate_otp()

        # Store OTP and get session token
        session_token = otp_service.store_otp(request.email, otp)

        # Send email in background using template
        background_tasks.add_task(
            email_service.send_otp_email,
            to_email=request.email,
            otp=otp,
            recipient_name=request.name
        )

        logger.info(f"OTP send requested for email: {request.email}")

        return OTPSendResponse(
            message="OTP sent successfully to your email",
            session_token=session_token,
            expires_in_minutes=settings.OTP_EXPIRY_MINUTES
        )

    except Exception as e:
        logger.error(f"Error sending OTP: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP. Please try again later."
        )


@router.post("/verify", response_model=OTPVerifyResponse)
async def verify_otp(request: OTPVerifyRequest):
    """
    Verify OTP code using session token
    """
    # verify_otp now returns (is_valid, message, email)
    is_valid, message, email = otp_service.verify_otp(request.session_token, request.otp)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    return OTPVerifyResponse(
        success=True,
        message=message,
        email=email
    )


@router.post("/cleanup")
async def cleanup_expired_otps():
    """
    Cleanup expired OTPs (admin endpoint)
    """
    otp_service.cleanup_expired_otps()
    return {"message": "Expired OTPs cleaned up successfully"}

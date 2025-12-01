import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailService:
    """
    Email service for sending emails via Gmail SMTP with Jinja2 templates
    """

    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.SMTP_FROM_EMAIL
        self.from_name = settings.SMTP_FROM_NAME

        # Setup Jinja2 template environment
        template_dir = Path(__file__).parent.parent / "templates" / "emails"
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def send_email(
            self,
            to_email: str,
            subject: str,
            html_content: str,
            text_content: str = None
    ) -> bool:
        """
        Send email using Gmail SMTP

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of email
            text_content: Plain text fallback (optional)

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email

            # Add plain text version if provided
            if text_content:
                part1 = MIMEText(text_content, "plain")
                message.attach(part1)

            # Add HTML version
            part2 = MIMEText(html_content, "html")
            message.attach(part2)

            # Connect to Gmail SMTP server
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()  # Enable TLS
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(message)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False

    def render_template(self, template_name: str, **context) -> str:
        """
        Render Jinja2 template with context

        Args:
            template_name: Name of the template file (e.g., 'otp_verification.html')
            **context: Template variables

        Returns:
            str: Rendered HTML content
        """
        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            logger.error(f"Failed to render template {template_name}: {str(e)}")
            raise

    def send_otp_email(self, to_email: str, otp: str, recipient_name: str = "User") -> bool:
        """
        Send OTP verification email

        Args:
            to_email: Recipient email
            otp: OTP code
            recipient_name: Recipient's name

        Returns:
            bool: Success status
        """
        html_content = self.render_template(
            "otp_verification.html",
            name=recipient_name,
            otp=otp,
            app_name=settings.APP_NAME,
            expiry_minutes=settings.OTP_EXPIRY_MINUTES
        )

        text_content = f"""
        Hello {recipient_name},

        Your verification code is: {otp}

        This code will expire in {settings.OTP_EXPIRY_MINUTES} minutes.

        If you didn't request this code, please ignore this email.

        Best regards,
        {settings.APP_NAME}
        """

        return self.send_email(
            to_email=to_email,
            subject=f"Your {settings.APP_NAME} Verification Code",
            html_content=html_content,
            text_content=text_content
        )

    def send_welcome_email(
            self,
            to_email: str,
            recipient_name: str,
            organization_name: str,
            login_url: str = "#"
    ) -> bool:
        """
        Send welcome email to new user

        Args:
            to_email: Recipient email
            recipient_name: Recipient's name
            organization_name: Organization name
            login_url: Login URL

        Returns:
            bool: Success status
        """
        html_content = self.render_template(
            "welcome.html",
            name=recipient_name,
            app_name=settings.APP_NAME,
            organization_name=organization_name,
            login_url=login_url
        )

        return self.send_email(
            to_email=to_email,
            subject=f"Welcome to {settings.APP_NAME}!",
            html_content=html_content
        )


# Create singleton instance
email_service = EmailService()

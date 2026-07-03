from datetime import datetime
from typing import Optional
import smtplib
from email.message import EmailMessage

from app.core.config import settings


async def send_email(to: str, subject: str, body: str) -> None:
    """Send email. If SMTP settings are present, use SMTP, otherwise log to console.

    This function is safe for development and will not raise on send failure — it
    will print an error to the logs. In production, replace with robust sending
    and retries (or use SendGrid/Amazon SES).
    """
    if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:
        try:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = settings.SMTP_FROM or settings.SMTP_USER
            msg["To"] = to
            msg.set_content(body)

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT or 25) as smtp:
                if settings.SMTP_TLS:
                    smtp.starttls()
                if settings.SMTP_USER:
                    smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                smtp.send_message(msg)
            print(f"Email sent to {to} via SMTP")
            return
        except Exception as e:
            print(f"Warning: SMTP send failed: {e}")

    # Fallback: print to console for development
    print("--- Sending email (dev stub) ---")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(body)
    print("--- End email ---")


def build_verification_link(token: str) -> str:
    return f"{settings.FRONTEND_URL.rstrip('/')}/verify-email?token={token}"


def build_reset_link(token: str) -> str:
    return f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={token}"

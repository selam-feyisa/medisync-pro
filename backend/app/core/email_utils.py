from datetime import datetime
from typing import Optional

from app.core.config import settings


async def send_email(to: str, subject: str, body: str) -> None:
    """Stub email sender for development — prints to console.

    Replace with real SMTP/SendGrid integration in production.
    """
    # For development we simply print the email contents to the server logs.
    print("--- Sending email (dev stub) ---")
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(body)
    print("--- End email ---")


def build_verification_link(token: str) -> str:
    return f"{settings.FRONTEND_URL.rstrip('/')}/verify-email?token={token}"


def build_reset_link(token: str) -> str:
    return f"{settings.FRONTEND_URL.rstrip('/')}/reset-password?token={token}"

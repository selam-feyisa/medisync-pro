"""Utility functions for common operations."""

from datetime import datetime, timedelta, timezone
from typing import Optional


def get_date_range(days: int = 7) -> tuple[datetime, datetime]:
    """Get date range for last N days."""
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def parse_iso_date(date_string: str) -> Optional[datetime]:
    """Parse ISO format date string."""
    try:
        return datetime.fromisoformat(date_string.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def format_date(date: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime to string."""
    return date.strftime(format_str)


def pagination_params(skip: int = 0, limit: int = 20) -> dict:
    """Calculate pagination skip and limit."""
    if limit > 100:
        limit = 100  # Max 100 per page
    if skip < 0:
        skip = 0

    return {"skip": skip, "limit": limit}


def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text."""
    return (
        text.lower()
        .strip()
        .replace(" ", "-")
        .replace("_", "-")
        .replace(".", "-")
        .replace("/", "-")
    )

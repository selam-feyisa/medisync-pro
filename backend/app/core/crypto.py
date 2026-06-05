from cryptography.fernet import Fernet
from backend.app.core.config import settings

def get_fernet() -> Fernet:
    """Return Fernet instance using ENCRYPTION_KEY from settings."""
    return Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_phi(value: str) -> str:
    """Encrypt a PHI string before saving to the database.
    PHI includes: date_of_birth, phone, insurance_number.
    """
    if not value:
        return value
    return get_fernet().encrypt(value.encode()).decode()

def decrypt_phi(value: str) -> str:
    """Decrypt a PHI string retrieved from the database."""
    if not value:
        return value
    return get_fernet().decrypt(value.encode()).decode()
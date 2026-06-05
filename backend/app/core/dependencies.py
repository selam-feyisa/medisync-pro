from backend.app.schemas.user import UserResponse


async def get_current_user():
    # TEMP USER (later we connect JWT auth)
    return UserResponse(
        id="123e4567-e89b-12d3-a456-426614174000",
        email="user@example.com",
        full_name="Demo User",
        phone_encrypted=None,
        mfa_enabled=False,
        auth_provider="local"
    )
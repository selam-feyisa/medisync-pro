from fastapi import APIRouter, Depends
from backend.app.schemas.user import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Profile"]
)

# TEMP MOCK USER (later we connect DB + auth)
def get_current_user():
    return {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "email": "user@example.com",
        "full_name": "Demo User",
        "phone_encrypted": None,
        "mfa_enabled": False,
        "auth_provider": "local"
    }


@router.get("/me", response_model=UserResponse)
async def get_my_profile():
    return get_current_user()
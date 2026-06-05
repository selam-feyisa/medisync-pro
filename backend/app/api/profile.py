from fastapi import APIRouter, Depends
from backend.app.schemas.user import UserResponse
from backend.app.core.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Profile"])


@router.get("/me", response_model=UserResponse)
async def get_my_profile(user=Depends(get_current_user)):
    return user
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Profile"]
)

@router.get("/me")
async def get_my_profile():
    return {
        "id": 1,
        "email": "user@example.com",
        "full_name": "Demo User",
        "role": "member"
    }
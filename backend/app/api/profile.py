from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Profile"]
)

@router.get("/me")
async def get_my_profile():
    return {
        "message": "Profile endpoint working"
    }
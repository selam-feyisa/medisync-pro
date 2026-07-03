from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession

# Core
from app.core.config import settings
from app.core.database import get_db

# Routers
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.workspace import router as workspace_router
from app.api.member import router as member_router
from app.api.project import router as project_router
from app.api.board import router as board_router
from app.api.column import router as column_router
from app.api.sprint import router as sprint_router
from app.api.ticket import router as ticket_router
from app.api.comment import router as comment_router
from app.api.label import router as label_router
from app.api.ticket_assignee import router as ticket_assignee_router
from app.api.ticket_label import router as ticket_label_router
from app.api.search import router as search_router
from app.api.time_entry import router as time_entry_router
from app.api.file_attachment import router as file_attachment_router

app = FastAPI(
    title="MediSync Pro",
    version="1.0.0",
    description="Healthcare Appointment & Project Management SaaS Platform",
    openapi_url="/api/v1/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== API ROUTERS ====================
app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(profile_router, prefix="/api/v1", tags=["Profile"])
app.include_router(workspace_router, prefix="/api/v1/workspaces", tags=["Workspaces"])
app.include_router(member_router, prefix="/api/v1", tags=["Members"])
app.include_router(project_router, prefix="/api/v1", tags=["Projects"])
app.include_router(board_router, prefix="/api/v1", tags=["Boards"])
app.include_router(column_router, prefix="/api/v1", tags=["Columns"])
app.include_router(sprint_router, prefix="/api/v1", tags=["Sprints"])
app.include_router(ticket_router, prefix="/api/v1", tags=["Tickets"])
app.include_router(comment_router, prefix="/api/v1", tags=["Comments"])
app.include_router(label_router, prefix="/api/v1", tags=["Labels"])
app.include_router(ticket_assignee_router, prefix="/api/v1", tags=["Ticket Assignees"])
app.include_router(ticket_label_router, prefix="/api/v1", tags=["Ticket Labels"])
app.include_router(search_router, prefix="/api/v1", tags=["Search"])
app.include_router(time_entry_router, prefix="/api/v1", tags=["Time Tracking"])
app.include_router(file_attachment_router, prefix="/api/v1", tags=["Attachments"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


# Development Seed Endpoint
@app.post("/seed", tags=["Development"])
async def run_seed(db: AsyncSession = Depends(get_db)):
    """Development only - Seed demo tickets"""
    try:
        from scripts.seed_demo import seed_demo_tickets
        await seed_demo_tickets(db, {"todo": None, "in_progress": None, "review": None})
        return {"status": "success", "message": "Demo data seeded successfully!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.on_event("startup")
async def initialize_services():
    """Initialize external service dependencies when the API starts."""
    try:
        from app.services.file_attachment import ensure_bucket_exists
        ensure_bucket_exists()
    except Exception as e:
        print(f"Warning: Could not initialize services: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

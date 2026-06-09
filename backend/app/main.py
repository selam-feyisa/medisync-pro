from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.core.config import settings
from backend.app.api.auth import router as auth_router
from backend.app.api.profile import router as profile_router
from backend.app.api.workspace import router as workspace_router
from backend.app.api.member import router as member_router
from backend.app.api.project import router as project_router
from backend.app.api.board import router as board_router
from backend.app.api.column import router as column_router
from backend.app.api.sprint import router as sprint_router
from backend.app.api.ticket import router as ticket_router
from backend.app.api.comment import router as comment_router
from backend.app.api.label import router as label_router

app = FastAPI(
    title="MediSync Pro",
    version="1.0.0",
    description="Healthcare Appointment & Project Management SaaS Platform",
    openapi_url="/api/v1/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "*"],  # Change "*" to specific domains in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
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

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
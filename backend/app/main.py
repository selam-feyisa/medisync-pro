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
from backend.app.api.sprint import router as sprint_router
# Add more as we implement

app = FastAPI(
    title="MediSync Pro",
    version="1.0.0",
    description="Healthcare Appointment & Project Management SaaS",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])
app.include_router(profile_router, prefix="/api/v1", tags=["profile"])
app.include_router(workspace_router, prefix="/api/v1", tags=["workspaces"])
app.include_router(member_router, prefix="/api/v1", tags=["members"])
app.include_router(project_router, prefix="/api/v1", tags=["projects"])
app.include_router(board_router, prefix="/api/v1", tags=["boards"])
app.include_router(sprint_router, prefix="/api/v1", tags=["sprints"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "medisync-pro"}

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
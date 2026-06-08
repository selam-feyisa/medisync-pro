from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.auth import router as auth_router
from backend.app.api.profile import router as profile_router
from backend.app.api.workspace import router as workspace_router
from backend.app.api.member import router as member_router
from backend.app.api.sprint import router as sprint_router
from backend.app.api.board import router as board_router
from backend.app.api.column import router as column_router
from backend.app.api.project import router as project_router

app = FastAPI(
    title="MediSync Pro",
    version="1.0.0",
    description="Healthcare Appointment and Records SaaS"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# AUTH ROUTES
app.include_router(auth_router, prefix="/api/v1")

# PROFILE ROUTES (IMPORTANT FIX)
app.include_router(profile_router, prefix="/api/v1")

# WORKSPACE ROUTES
app.include_router(workspace_router, prefix="/api/v1")

# MEMBER ROUTES
app.include_router(member_router, prefix="/api/v1")

# SPRINT ROUTES
app.include_router(sprint_router, prefix="/api/v1")

# BOARD ROUTES
app.include_router(board_router, prefix="/api/v1")

# COLUMN ROUTES
app.include_router(column_router, prefix="/api/v1")

# PROJECT ROUTES
app.include_router(project_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok", "service": "medisync-pro"}
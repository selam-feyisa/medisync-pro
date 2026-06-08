from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.auth import router as auth_router
from backend.app.api.profile import router as profile_router

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

@app.get("/health")
def health():
    return {"status": "ok", "service": "medisync-pro"}
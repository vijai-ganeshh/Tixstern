
from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
app = FastAPI(
    title="Tixstern API",
    description=(
        "A concert ticketing platform focused on "
        "concurrency-safe bookings and reliable inventory."
    ),
    version="0.1.0",
)
app.include_router(auth_router, prefix="/api/v1")

@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """Check whether the API application is responding."""
    return {
        "status": "healthy",
        "service": "Tixstern API",
        "version": "0.1.0",
    }


from fastapi import FastAPI

app = FastAPI(
    title="Tixstern API",
    description=(
        "A concert ticketing platform focused on "
        "concurrency-safe bookings and reliable inventory."
    ),
    version="0.1.0",
)


@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """Check whether the API application is responding."""
    return {
        "status": "healthy",
        "service": "Tixstern API",
        "version": "0.1.0",
    }

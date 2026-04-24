"""Health check route for the application."""

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/health", tags=["Health"])


@router.get("")
def health_check() -> dict[str, str]:
    """Return a simple health status response."""
    return {"status": "ok", "message": "SensorVision backend is running."}

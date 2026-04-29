"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.files import router as files_router
from app.api.routes.health import router as health_router
from app.api.routes.image_processing import router as image_processing_router
from app.api.routes.signal_analysis import router as signal_analysis_router
from app.api.routes.uploads import router as uploads_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(uploads_router)
app.include_router(files_router)
app.include_router(image_processing_router)
app.include_router(signal_analysis_router)


@app.get("/")
def root() -> dict[str, str]:
    """Return a root message for the API."""
    return {"message": "Welcome to SensorVision Workbench API."}

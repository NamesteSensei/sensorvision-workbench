"""System information routes."""

from fastapi import APIRouter

from app.core.config import settings
from app.core.constants import (
    FILE_CATEGORY_TO_ALLOWED_EXTENSIONS,
    FILE_CATEGORY_TO_MAX_SIZE,
)
from app.schemas.system_info import SystemInfoResponse, UploadLimit

router = APIRouter(prefix="/api/v1/system", tags=["System"])


@router.get("/info", response_model=SystemInfoResponse)
def get_system_info() -> SystemInfoResponse:
    """Return application system information and settings."""
    upload_limits = []

    for category, max_size_bytes in FILE_CATEGORY_TO_MAX_SIZE.items():
        upload_limits.append(
            UploadLimit(
                category=category,
                max_size_mb=round(max_size_bytes / (1024 * 1024), 2),
                allowed_extensions=sorted(
                    FILE_CATEGORY_TO_ALLOWED_EXTENSIONS[category],
                ),
            ),
        )

    return SystemInfoResponse(
        app_name=settings.app_name,
        app_version=settings.app_version,
        api_status="online",
        storage_mode="local disk",
        api_docs_url="http://127.0.0.1:8000/docs",
        default_yolo_model="yolov8n.pt",
        supported_yolo_models=["yolov8n.pt", "yolov8s.pt"],
        supported_trackers=["bytetrack.yaml", "botsort.yaml"],
        upload_limits=upload_limits,
        security_features=[
            "File extension validation",
            "File size limits",
            "UUID-based filenames",
            "Filename sanitization",
            "Controlled local storage directories",
            "Protected file-serving paths",
            "Pydantic request validation",
            "Restricted CORS configuration",
        ],
    )

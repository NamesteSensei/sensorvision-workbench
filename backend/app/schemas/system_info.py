"""Schemas for system information and settings."""

from pydantic import BaseModel


class UploadLimit(BaseModel):
    """Upload limit information."""

    category: str
    max_size_mb: float
    allowed_extensions: list[str]


class SystemInfoResponse(BaseModel):
    """System information response."""

    app_name: str
    app_version: str
    api_status: str
    storage_mode: str
    api_docs_url: str
    default_yolo_model: str
    supported_yolo_models: list[str]
    supported_trackers: list[str]
    upload_limits: list[UploadLimit]
    security_features: list[str]

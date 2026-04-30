"""Schemas for aerial image analysis."""

from pydantic import BaseModel, Field


class AerialAnalysisResponse(BaseModel):
    """Response returned after aerial image analysis completes."""

    job_id: str
    original_file_name: str
    stored_file_name: str
    processed_file_name: str
    file_category: str
    model_name: str
    confidence_threshold: float
    detected_object_count: int
    class_counts: dict[str, int]
    processed_image_url: str
    file_size_bytes: int
    message: str


class AerialAnalysisOptions(BaseModel):
    """Aerial analysis options submitted by the user."""

    model_name: str = Field(default="yolov8n.pt")
    confidence_threshold: float = Field(default=0.25, ge=0.0, le=1.0)
    iou_threshold: float = Field(default=0.45, ge=0.0, le=1.0)

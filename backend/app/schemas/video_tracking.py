"""Schemas for video object detection and tracking."""

from enum import Enum

from pydantic import BaseModel, Field


class TrackerName(str, Enum):
    """Supported YOLO tracker configuration names."""

    bytetrack = "bytetrack.yaml"
    botsort = "botsort.yaml"


class VideoTrackingResponse(BaseModel):
    """Response returned after video tracking completes."""

    job_id: str
    original_file_name: str
    stored_file_name: str
    processed_file_name: str
    file_category: str
    model_name: str
    tracker_name: TrackerName
    confidence_threshold: float
    frame_count: int
    fps: float
    unique_track_count: int
    class_counts: dict[str, int]
    processed_video_url: str
    file_size_bytes: int
    message: str


class VideoTrackingOptions(BaseModel):
    """Video tracking options submitted by the user."""

    model_name: str = Field(default="yolov8n.pt")
    tracker_name: TrackerName = Field(default=TrackerName.bytetrack)
    confidence_threshold: float = Field(default=0.25, ge=0.0, le=1.0)
    iou_threshold: float = Field(default=0.45, ge=0.0, le=1.0)

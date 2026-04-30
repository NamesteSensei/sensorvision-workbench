"""Video tracking routes."""

from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.video_tracking import (
    TrackerName,
    VideoTrackingOptions,
    VideoTrackingResponse,
)
from app.services.video_tracking_service import VideoTrackingService

router = APIRouter(
    prefix="/api/v1/video-tracking",
    tags=["Video Tracking"],
)


@router.post("/track", response_model=VideoTrackingResponse)
async def track_video(
    upload_file: UploadFile = File(...),
    model_name: str = Form(default="yolov8n.pt"),
    tracker_name: TrackerName = Form(default=TrackerName.bytetrack),
    confidence_threshold: float = Form(default=0.25),
    iou_threshold: float = Form(default=0.45),
) -> VideoTrackingResponse:
    """Track objects in an uploaded video."""
    options = VideoTrackingOptions(
        model_name=model_name,
        tracker_name=tracker_name,
        confidence_threshold=confidence_threshold,
        iou_threshold=iou_threshold,
    )

    service = VideoTrackingService()
    return await service.track_uploaded_video(
        upload_file=upload_file,
        options=options,
    )

"""Aerial image analysis routes."""

from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.aerial_analysis import (
    AerialAnalysisOptions,
    AerialAnalysisResponse,
)
from app.services.aerial_analysis_service import AerialAnalysisService

router = APIRouter(
    prefix="/api/v1/aerial-analysis",
    tags=["Aerial Analysis"],
)


@router.post("/analyze", response_model=AerialAnalysisResponse)
async def analyze_aerial_image(
    upload_file: UploadFile = File(...),
    model_name: str = Form(default="yolov8n.pt"),
    confidence_threshold: float = Form(default=0.25),
    iou_threshold: float = Form(default=0.45),
) -> AerialAnalysisResponse:
    """Analyze an uploaded aerial image with YOLO."""
    options = AerialAnalysisOptions(
        model_name=model_name,
        confidence_threshold=confidence_threshold,
        iou_threshold=iou_threshold,
    )

    service = AerialAnalysisService()
    return await service.analyze_uploaded_aerial_image(
        upload_file=upload_file,
        options=options,
    )

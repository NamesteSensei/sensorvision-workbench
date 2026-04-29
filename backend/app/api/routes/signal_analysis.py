"""Signal analysis routes."""

from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.signal_analysis import (
    SignalAnalysisOptions,
    SignalAnalysisResponse,
)
from app.services.signal_analysis_service import SignalAnalysisService

router = APIRouter(
    prefix="/api/v1/signal-analysis",
    tags=["Signal Analysis"],
)


@router.post("/analyze", response_model=SignalAnalysisResponse)
async def analyze_signal(
    upload_file: UploadFile = File(...),
    selected_column: str = Form(default="value"),
    sampling_rate_hz: float = Form(default=1.0),
    smoothing_window: int = Form(default=5),
) -> SignalAnalysisResponse:
    """Analyze an uploaded CSV signal file."""
    options = SignalAnalysisOptions(
        selected_column=selected_column,
        sampling_rate_hz=sampling_rate_hz,
        smoothing_window=smoothing_window,
    )

    service = SignalAnalysisService()
    return await service.analyze_uploaded_signal(
        upload_file=upload_file,
        options=options,
    )

"""Schemas for signal analysis requests and responses."""

from pydantic import BaseModel, Field


class SignalAnalysisResponse(BaseModel):
    """Response returned after signal analysis completes."""

    job_id: str
    original_file_name: str
    stored_file_name: str
    file_category: str
    selected_column: str
    sample_count: int
    sampling_rate_hz: float
    smoothing_window: int
    time_plot_url: str
    frequency_plot_url: str
    file_size_bytes: int
    message: str


class SignalAnalysisOptions(BaseModel):
    """Signal analysis options submitted by the user."""

    selected_column: str = Field(default="value")
    sampling_rate_hz: float = Field(default=1.0, gt=0.0, le=1_000_000.0)
    smoothing_window: int = Field(default=5, ge=1, le=501)

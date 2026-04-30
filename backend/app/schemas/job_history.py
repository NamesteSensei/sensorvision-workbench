"""Schemas for job history and dashboard summaries."""

from typing import Any

from pydantic import BaseModel


class JobHistoryRecord(BaseModel):
    """Stored processing job history record."""

    job_id: str
    job_type: str
    original_file_name: str
    output_file_name: str
    output_url: str
    created_at: str
    summary: dict[str, Any]


class JobHistoryResponse(BaseModel):
    """Response containing job history records."""

    jobs: list[JobHistoryRecord]


class DashboardSummaryResponse(BaseModel):
    """Dashboard summary response."""

    total_jobs: int
    image_jobs: int
    signal_jobs: int
    video_jobs: int
    aerial_jobs: int
    recent_jobs: list[JobHistoryRecord]

"""Routes for job history and dashboard summary."""

from fastapi import APIRouter

from app.schemas.job_history import (
    DashboardSummaryResponse,
    JobHistoryRecord,
    JobHistoryResponse,
)
from app.services.job_history_service import JobHistoryService

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])


@router.get("", response_model=JobHistoryResponse)
def list_jobs() -> JobHistoryResponse:
    """Return all saved processing jobs."""
    service = JobHistoryService()
    return service.list_job_records()


@router.get("/dashboard", response_model=DashboardSummaryResponse)
def get_dashboard_summary() -> DashboardSummaryResponse:
    """Return dashboard summary metrics."""
    service = JobHistoryService()
    return service.get_dashboard_summary()


@router.get("/{job_id}", response_model=JobHistoryRecord)
def get_job(job_id: str) -> JobHistoryRecord:
    """Return a saved processing job by ID."""
    service = JobHistoryService()
    return service.get_job_record(job_id)

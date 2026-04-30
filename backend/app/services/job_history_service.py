"""Service for saving and reading processing job history."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import HTTPException, status

from app.core.constants import JOB_RECORDS_DIR
from app.schemas.job_history import (
    DashboardSummaryResponse,
    JobHistoryRecord,
    JobHistoryResponse,
)


class JobHistoryService:
    """Service responsible for local JSON job history records."""

    def __init__(self) -> None:
        """Initialize job history service."""
        JOB_RECORDS_DIR.mkdir(parents=True, exist_ok=True)

    def save_job_record(
        self,
        job_id: str,
        job_type: str,
        original_file_name: str,
        output_file_name: str,
        output_url: str,
        summary: dict[str, Any],
    ) -> JobHistoryRecord:
        """Save a processing job record to disk."""
        record = JobHistoryRecord(
            job_id=job_id,
            job_type=job_type,
            original_file_name=original_file_name,
            output_file_name=output_file_name,
            output_url=output_url,
            created_at=datetime.now(timezone.utc).isoformat(),
            summary=summary,
        )

        record_path = self._get_record_path(job_id)
        record_path.write_text(
            json.dumps(record.model_dump(), indent=2),
            encoding="utf-8",
        )

        return record

    def list_job_records(self) -> JobHistoryResponse:
        """Return all job history records sorted newest first."""
        records = self._load_all_records()
        sorted_records = sorted(
            records,
            key=lambda record: record.created_at,
            reverse=True,
        )
        return JobHistoryResponse(jobs=sorted_records)

    def get_dashboard_summary(self) -> DashboardSummaryResponse:
        """Return dashboard summary metrics."""
        records = self._load_all_records()

        image_jobs = sum(1 for record in records if record.job_type == "image")
        signal_jobs = sum(1 for record in records if record.job_type == "signal")
        video_jobs = sum(1 for record in records if record.job_type == "video")
        aerial_jobs = sum(1 for record in records if record.job_type == "aerial")

        recent_jobs = sorted(
            records,
            key=lambda record: record.created_at,
            reverse=True,
        )[:5]

        return DashboardSummaryResponse(
            total_jobs=len(records),
            image_jobs=image_jobs,
            signal_jobs=signal_jobs,
            video_jobs=video_jobs,
            aerial_jobs=aerial_jobs,
            recent_jobs=recent_jobs,
        )

    def get_job_record(self, job_id: str) -> JobHistoryRecord:
        """Return one job history record by job ID."""
        record_path = self._get_record_path(job_id)

        if not record_path.exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job record not found.",
            )

        return self._load_record(record_path)

    def _get_record_path(self, job_id: str) -> Path:
        """Return path for a job record."""
        return JOB_RECORDS_DIR / f"{job_id}.json"

    def _load_all_records(self) -> list[JobHistoryRecord]:
        """Load all valid job records."""
        records: list[JobHistoryRecord] = []

        for record_path in JOB_RECORDS_DIR.glob("*.json"):
            try:
                records.append(self._load_record(record_path))
            except (json.JSONDecodeError, ValueError):
                continue

        return records

    def _load_record(self, record_path: Path) -> JobHistoryRecord:
        """Load one job history record from disk."""
        raw_data = json.loads(record_path.read_text(encoding="utf-8"))
        return JobHistoryRecord(**raw_data)

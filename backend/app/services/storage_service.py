"""Local storage service for uploaded and generated files."""

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.constants import (
    FILE_CATEGORY_TO_INPUT_DIR,
    JOB_RECORDS_DIR,
    OUTPUTS_DIR,
    PREVIEWS_DIR,
    TEMP_DIR,
)
from app.utils.validation_utils import sanitize_file_name


class StorageService:
    """Service responsible for safe local file storage."""

    def __init__(self) -> None:
        """Initialize storage service and ensure directories exist."""
        self.ensure_storage_directories()

    def ensure_storage_directories(self) -> None:
        """Create required storage directories if they do not exist."""
        directories = [
            *FILE_CATEGORY_TO_INPUT_DIR.values(),
            OUTPUTS_DIR,
            PREVIEWS_DIR,
            TEMP_DIR,
            JOB_RECORDS_DIR,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def create_job_id(self) -> str:
        """Create a unique job identifier."""
        return uuid4().hex

    def build_stored_file_name(
        self,
        original_file_name: str,
        job_id: str,
    ) -> str:
        """Build a safe stored file name using a job ID."""
        safe_original_name = sanitize_file_name(original_file_name)
        return f"{job_id}_{safe_original_name}"

    def get_input_directory(self, file_category: str) -> Path:
        """Return the input directory for a file category."""
        return FILE_CATEGORY_TO_INPUT_DIR[file_category]

    async def save_upload_file(
        self,
        upload_file: UploadFile,
        file_category: str,
        job_id: str,
    ) -> Path:
        """Save an uploaded file and return its storage path."""
        input_directory = self.get_input_directory(file_category)
        stored_file_name = self.build_stored_file_name(
            upload_file.filename or "uploaded_file",
            job_id,
        )
        destination_path = input_directory / stored_file_name

        with destination_path.open("wb") as output_file:
            while chunk := await upload_file.read(1024 * 1024):
                output_file.write(chunk)

        await upload_file.seek(0)
        return destination_path

    def build_file_url(self, file_path: Path) -> str:
        """Build a URL path for a locally stored file."""
        relative_path = file_path.relative_to(file_path.parents[3])
        return f"/{relative_path.as_posix()}"

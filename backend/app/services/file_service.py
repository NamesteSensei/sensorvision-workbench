"""File service for secure upload handling."""

from pathlib import Path

from fastapi import UploadFile

from app.schemas.common import UploadedFileResponse
from app.services.storage_service import StorageService
from app.utils.validation_utils import (
    validate_file_extension,
    validate_file_size,
)


class FileService:
    """Service responsible for validating and saving uploaded files."""

    def __init__(self) -> None:
        """Initialize the file service."""
        self.storage_service = StorageService()

    async def save_validated_upload(
        self,
        upload_file: UploadFile,
        file_category: str,
    ) -> UploadedFileResponse:
        """Validate and save an uploaded file."""
        original_file_name = upload_file.filename or "uploaded_file"

        validate_file_extension(original_file_name, file_category)
        file_size_bytes = await validate_file_size(upload_file, file_category)

        job_id = self.storage_service.create_job_id()
        stored_file_path = await self.storage_service.save_upload_file(
            upload_file=upload_file,
            file_category=file_category,
            job_id=job_id,
        )

        return UploadedFileResponse(
            job_id=job_id,
            original_file_name=original_file_name,
            stored_file_name=Path(stored_file_path).name,
            file_category=file_category,
            file_size_bytes=file_size_bytes,
            file_url=self.storage_service.build_file_url(stored_file_path),
            message="File uploaded successfully.",
        )

"""Upload routes for secure local file handling."""

from fastapi import APIRouter, File, UploadFile

from app.schemas.common import UploadedFileResponse
from app.services.file_service import FileService

router = APIRouter(prefix="/api/v1/uploads", tags=["Uploads"])


@router.post("/{file_category}", response_model=UploadedFileResponse)
async def upload_file(
    file_category: str,
    upload_file: UploadFile = File(...),
) -> UploadedFileResponse:
    """Upload and store a validated file."""
    file_service = FileService()
    return await file_service.save_validated_upload(
        upload_file=upload_file,
        file_category=file_category,
    )

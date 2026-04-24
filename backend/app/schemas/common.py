"""Common response schemas used across the API."""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Standard message response."""

    message: str


class UploadedFileResponse(BaseModel):
    """Response returned after a file is uploaded successfully."""

    job_id: str
    original_file_name: str
    stored_file_name: str
    file_category: str
    file_size_bytes: int
    file_url: str
    message: str

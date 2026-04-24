"""File routes for serving locally stored files."""

from pathlib import Path

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from app.core.constants import DATA_DIR

router = APIRouter(prefix="/api/v1/files", tags=["Files"])


@router.get("/{file_path:path}")
def get_file(file_path: str) -> FileResponse:
    """Return a stored local file by relative path."""
    requested_path = (DATA_DIR.parent / file_path).resolve()
    allowed_root = DATA_DIR.resolve()

    if not str(requested_path).startswith(str(allowed_root)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access to this file path is forbidden.",
        )

    if not requested_path.exists() or not requested_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found.",
        )

    return FileResponse(requested_path)

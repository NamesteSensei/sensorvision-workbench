"""Validation utilities for uploaded files."""

from pathlib import Path

from fastapi import HTTPException, UploadFile, status

from app.core.constants import (
    FILE_CATEGORY_TO_ALLOWED_EXTENSIONS,
    FILE_CATEGORY_TO_MAX_SIZE,
)


def get_file_extension(file_name: str) -> str:
    """Return the lowercase extension from a file name."""
    return Path(file_name).suffix.lower()


def validate_file_category(file_category: str) -> None:
    """Validate that the file category is supported."""
    if file_category not in FILE_CATEGORY_TO_ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file category: {file_category}",
        )


def validate_file_extension(file_name: str, file_category: str) -> None:
    """Validate that a file extension is allowed for the category."""
    validate_file_category(file_category)

    file_extension = get_file_extension(file_name)
    allowed_extensions = FILE_CATEGORY_TO_ALLOWED_EXTENSIONS[file_category]

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported file type '{file_extension}' for "
                f"category '{file_category}'."
            ),
        )


async def validate_file_size(
    upload_file: UploadFile,
    file_category: str,
) -> int:
    """Validate uploaded file size and return the size in bytes."""
    validate_file_category(file_category)

    max_size_bytes = FILE_CATEGORY_TO_MAX_SIZE[file_category]
    file_bytes = await upload_file.read()
    file_size_bytes = len(file_bytes)

    await upload_file.seek(0)

    if file_size_bytes == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if file_size_bytes > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=(
                f"File is too large. Maximum allowed size is "
                f"{max_size_bytes} bytes."
            ),
        )

    return file_size_bytes


def sanitize_file_name(file_name: str) -> str:
    """Return a safe version of the original file name."""
    safe_characters = []

    for character in file_name:
        if character.isalnum() or character in {".", "-", "_"}:
            safe_characters.append(character)
        else:
            safe_characters.append("_")

    sanitized_name = "".join(safe_characters).strip("._")

    if not sanitized_name:
        return "uploaded_file"

    return sanitized_name

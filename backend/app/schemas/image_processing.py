"""Schemas for image processing requests and responses."""

from enum import Enum

from pydantic import BaseModel, Field


class ImageFilterName(str, Enum):
    """Supported image enhancement filters."""

    gaussian = "gaussian"
    median = "median"
    bilateral = "bilateral"


class ImageProcessingResponse(BaseModel):
    """Response returned after image processing completes."""

    job_id: str
    original_file_name: str
    stored_file_name: str
    processed_file_name: str
    file_category: str
    filter_name: ImageFilterName
    processed_image_url: str
    file_size_bytes: int
    message: str


class ImageProcessingOptions(BaseModel):
    """Image processing options submitted by the user."""

    filter_name: ImageFilterName = Field(default=ImageFilterName.gaussian)
    kernel_size: int = Field(default=5, ge=3, le=31)
    sigma_value: float = Field(default=1.0, ge=0.0, le=10.0)

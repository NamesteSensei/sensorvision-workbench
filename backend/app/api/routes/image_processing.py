"""Image processing routes."""

from fastapi import APIRouter, File, Form, UploadFile

from app.schemas.image_processing import (
    ImageFilterName,
    ImageProcessingOptions,
    ImageProcessingResponse,
)
from app.services.image_processing_service import ImageProcessingService

router = APIRouter(
    prefix="/api/v1/image-processing",
    tags=["Image Processing"],
)


@router.post("/enhance", response_model=ImageProcessingResponse)
async def enhance_image(
    upload_file: UploadFile = File(...),
    filter_name: ImageFilterName = Form(default=ImageFilterName.gaussian),
    kernel_size: int = Form(default=5),
    sigma_value: float = Form(default=1.0),
) -> ImageProcessingResponse:
    """Enhance an uploaded image with the selected filter."""
    options = ImageProcessingOptions(
        filter_name=filter_name,
        kernel_size=kernel_size,
        sigma_value=sigma_value,
    )

    service = ImageProcessingService()
    return await service.process_uploaded_image(
        upload_file=upload_file,
        options=options,
    )

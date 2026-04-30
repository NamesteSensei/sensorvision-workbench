"""Image processing service using OpenCV."""

import cv2
from fastapi import HTTPException, UploadFile, status

from app.core.constants import IMAGE_OUTPUT_DIR
from app.schemas.image_processing import (
    ImageFilterName,
    ImageProcessingOptions,
    ImageProcessingResponse,
)
from app.services.file_service import FileService
from app.services.job_history_service import JobHistoryService
from app.services.storage_service import StorageService


class ImageProcessingService:
    """Service responsible for image enhancement operations."""

    def __init__(self) -> None:
        """Initialize image processing service dependencies."""
        self.file_service = FileService()
        self.storage_service = StorageService()
        self.job_history_service = JobHistoryService()

    async def process_uploaded_image(
        self,
        upload_file: UploadFile,
        options: ImageProcessingOptions,
    ) -> ImageProcessingResponse:
        """Validate, save, process, and return an uploaded image."""
        upload_response = await self.file_service.save_validated_upload(
            upload_file=upload_file,
            file_category="image",
        )

        input_path = (
            self.storage_service.get_input_directory("image")
            / upload_response.stored_file_name
        )

        image = cv2.imread(str(input_path))

        if image is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file could not be read as an image.",
            )

        processed_image = self.apply_filter(image, options)

        processed_file_name = (
            f"{upload_response.job_id}_{options.filter_name.value}_processed.png"
        )
        output_path = IMAGE_OUTPUT_DIR / processed_file_name
        output_path.parent.mkdir(parents=True, exist_ok=True)

        success = cv2.imwrite(str(output_path), processed_image)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save processed image.",
            )

        processed_image_url = self.storage_service.build_file_url(output_path)

        self.job_history_service.save_job_record(
            job_id=upload_response.job_id,
            job_type="image",
            original_file_name=upload_response.original_file_name,
            output_file_name=processed_file_name,
            output_url=processed_image_url,
            summary={
                "filter_name": options.filter_name.value,
                "file_size_bytes": upload_response.file_size_bytes,
            },
        )

        return ImageProcessingResponse(
            job_id=upload_response.job_id,
            original_file_name=upload_response.original_file_name,
            stored_file_name=upload_response.stored_file_name,
            processed_file_name=processed_file_name,
            file_category="image",
            filter_name=options.filter_name,
            processed_image_url=processed_image_url,
            file_size_bytes=upload_response.file_size_bytes,
            message="Image processed successfully.",
        )

    def apply_filter(
        self,
        image,
        options: ImageProcessingOptions,
    ):
        """Apply the selected OpenCV filter to an image."""
        kernel_size = self._make_odd_kernel_size(options.kernel_size)

        if options.filter_name == ImageFilterName.gaussian:
            return cv2.GaussianBlur(
                image,
                (kernel_size, kernel_size),
                options.sigma_value,
            )

        if options.filter_name == ImageFilterName.median:
            return cv2.medianBlur(image, kernel_size)

        if options.filter_name == ImageFilterName.bilateral:
            return cv2.bilateralFilter(
                image,
                d=kernel_size,
                sigmaColor=75,
                sigmaSpace=75,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported filter: {options.filter_name}",
        )

    def _make_odd_kernel_size(self, kernel_size: int) -> int:
        """Return a valid odd kernel size."""
        if kernel_size % 2 == 0:
            return kernel_size + 1

        return kernel_size

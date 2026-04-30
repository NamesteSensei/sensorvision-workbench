"""Aerial image analysis service using YOLO."""

import cv2
from fastapi import HTTPException, UploadFile, status

from app.core.constants import AERIAL_OUTPUT_DIR
from app.schemas.aerial_analysis import (
    AerialAnalysisOptions,
    AerialAnalysisResponse,
)
from app.services.file_service import FileService
from app.services.job_history_service import JobHistoryService
from app.services.storage_service import StorageService
from app.services.yolo_service import YoloService


class AerialAnalysisService:
    """Service responsible for aerial image analysis."""

    def __init__(self) -> None:
        """Initialize aerial analysis service dependencies."""
        self.file_service = FileService()
        self.storage_service = StorageService()
        self.yolo_service = YoloService()
        self.job_history_service = JobHistoryService()

    async def analyze_uploaded_aerial_image(
        self,
        upload_file: UploadFile,
        options: AerialAnalysisOptions,
    ) -> AerialAnalysisResponse:
        """Validate, save, analyze, and return an aerial image result."""
        upload_response = await self.file_service.save_validated_upload(
            upload_file=upload_file,
            file_category="aerial",
        )

        input_path = (
            self.storage_service.get_input_directory("aerial")
            / upload_response.stored_file_name
        )

        image = cv2.imread(str(input_path))

        if image is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file could not be read as an image.",
            )

        model = self.yolo_service.get_model(options.model_name)

        results = model.predict(
            source=str(input_path),
            conf=options.confidence_threshold,
            iou=options.iou_threshold,
            verbose=False,
        )

        if not results:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="YOLO did not return analysis results.",
            )

        result = results[0]
        annotated_image = result.plot()
        class_counts = self._build_class_counts(result)
        detected_object_count = sum(class_counts.values())

        AERIAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        processed_file_name = f"{upload_response.job_id}_aerial_detected.png"
        output_path = AERIAL_OUTPUT_DIR / processed_file_name

        success = cv2.imwrite(str(output_path), annotated_image)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save aerial analysis image.",
            )

        processed_image_url = self.storage_service.build_file_url(output_path)

        self.job_history_service.save_job_record(
            job_id=upload_response.job_id,
            job_type="aerial",
            original_file_name=upload_response.original_file_name,
            output_file_name=processed_file_name,
            output_url=processed_image_url,
            summary={
                "model_name": options.model_name,
                "confidence_threshold": options.confidence_threshold,
                "detected_object_count": detected_object_count,
                "class_counts": class_counts,
            },
        )

        return AerialAnalysisResponse(
            job_id=upload_response.job_id,
            original_file_name=upload_response.original_file_name,
            stored_file_name=upload_response.stored_file_name,
            processed_file_name=processed_file_name,
            file_category="aerial",
            model_name=options.model_name,
            confidence_threshold=options.confidence_threshold,
            detected_object_count=detected_object_count,
            class_counts=class_counts,
            processed_image_url=processed_image_url,
            file_size_bytes=upload_response.file_size_bytes,
            message="Aerial image analysis completed successfully.",
        )

    def _build_class_counts(self, result) -> dict[str, int]:
        """Build class-count summary from a YOLO image result."""
        boxes = result.boxes
        class_counts: dict[str, int] = {}

        if boxes is None or boxes.cls is None:
            return class_counts

        class_ids = boxes.cls.cpu().numpy().astype(int)

        for class_id in class_ids:
            class_name = result.names.get(class_id, str(class_id))
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        return class_counts

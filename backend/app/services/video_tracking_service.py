"""Video tracking service using Ultralytics YOLO and OpenCV."""

from pathlib import Path

import cv2
from fastapi import HTTPException, UploadFile, status

from app.core.constants import VIDEO_OUTPUT_DIR
from app.schemas.video_tracking import (
    VideoTrackingOptions,
    VideoTrackingResponse,
)
from app.services.file_service import FileService
from app.services.storage_service import StorageService
from app.services.yolo_service import YoloService


class VideoTrackingService:
    """Service responsible for video object detection and tracking."""

    def __init__(self) -> None:
        """Initialize video tracking service dependencies."""
        self.file_service = FileService()
        self.storage_service = StorageService()
        self.yolo_service = YoloService()

    async def track_uploaded_video(
        self,
        upload_file: UploadFile,
        options: VideoTrackingOptions,
    ) -> VideoTrackingResponse:
        """Validate, save, track, and return an uploaded video."""
        upload_response = await self.file_service.save_validated_upload(
            upload_file=upload_file,
            file_category="video",
        )

        input_path = (
            self.storage_service.get_input_directory("video")
            / upload_response.stored_file_name
        )

        video_metadata = self._read_video_metadata(input_path)

        VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        processed_file_name = f"{upload_response.job_id}_tracked.mp4"
        output_path = VIDEO_OUTPUT_DIR / processed_file_name

        tracking_metrics = self._process_video_with_yolo(
            input_path=input_path,
            output_path=output_path,
            options=options,
            fps=video_metadata["fps"],
            width=video_metadata["width"],
            height=video_metadata["height"],
        )

        return VideoTrackingResponse(
            job_id=upload_response.job_id,
            original_file_name=upload_response.original_file_name,
            stored_file_name=upload_response.stored_file_name,
            processed_file_name=processed_file_name,
            file_category="video",
            model_name=options.model_name,
            tracker_name=options.tracker_name,
            confidence_threshold=options.confidence_threshold,
            frame_count=video_metadata["frame_count"],
            fps=video_metadata["fps"],
            unique_track_count=tracking_metrics["unique_track_count"],
            class_counts=tracking_metrics["class_counts"],
            processed_video_url=self.storage_service.build_file_url(
                output_path,
            ),
            file_size_bytes=upload_response.file_size_bytes,
            message="Video tracking completed successfully.",
        )

    def _read_video_metadata(self, input_path: Path) -> dict[str, int | float]:
        """Read basic video metadata using OpenCV."""
        video_capture = cv2.VideoCapture(str(input_path))

        if not video_capture.isOpened():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file could not be opened as a video.",
            )

        fps = video_capture.get(cv2.CAP_PROP_FPS)
        width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))

        video_capture.release()

        if fps <= 0:
            fps = 30.0

        if width <= 0 or height <= 0 or frame_count <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Video metadata could not be read correctly.",
            )

        return {
            "fps": fps,
            "width": width,
            "height": height,
            "frame_count": frame_count,
        }

    def _process_video_with_yolo(
        self,
        input_path: Path,
        output_path: Path,
        options: VideoTrackingOptions,
        fps: float,
        width: int,
        height: int,
    ) -> dict[str, int | dict[str, int]]:
        """Run YOLO tracking and save annotated output video."""
        model = self.yolo_service.get_model(options.model_name)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(
            str(output_path),
            fourcc,
            fps,
            (width, height),
        )

        if not video_writer.isOpened():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create output video writer.",
            )

        class_counts: dict[str, int] = {}
        unique_track_ids: set[int] = set()

        try:
            results = model.track(
                source=str(input_path),
                stream=True,
                persist=True,
                conf=options.confidence_threshold,
                iou=options.iou_threshold,
                tracker=options.tracker_name.value,
                verbose=False,
            )

            for result in results:
                annotated_frame = result.plot()

                if annotated_frame.shape[1] != width:
                    annotated_frame = cv2.resize(
                        annotated_frame,
                        (width, height),
                    )

                video_writer.write(annotated_frame)
                self._update_tracking_metrics(
                    result=result,
                    class_counts=class_counts,
                    unique_track_ids=unique_track_ids,
                )

        except Exception as error:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Video tracking failed: {error}",
            ) from error
        finally:
            video_writer.release()

        if not output_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Processed video was not created.",
            )

        return {
            "class_counts": class_counts,
            "unique_track_count": len(unique_track_ids),
        }

    def _update_tracking_metrics(
        self,
        result,
        class_counts: dict[str, int],
        unique_track_ids: set[int],
    ) -> None:
        """Update class counts and unique track IDs from a YOLO result."""
        boxes = result.boxes

        if boxes is None or boxes.cls is None:
            return

        class_ids = boxes.cls.cpu().numpy().astype(int)

        for class_id in class_ids:
            class_name = result.names.get(class_id, str(class_id))
            class_counts[class_name] = class_counts.get(class_name, 0) + 1

        if boxes.id is None:
            return

        track_ids = boxes.id.cpu().numpy().astype(int)

        for track_id in track_ids:
            unique_track_ids.add(int(track_id))

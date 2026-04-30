"""YOLO model service for object detection and tracking."""

from ultralytics import YOLO


class YoloService:
    """Service responsible for loading and returning YOLO models."""

    _models: dict[str, YOLO] = {}

    def get_model(self, model_name: str) -> YOLO:
        """Return a cached YOLO model instance."""
        if model_name not in self._models:
            self._models[model_name] = YOLO(model_name)

        return self._models[model_name]

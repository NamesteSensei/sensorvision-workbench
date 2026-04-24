"""Application constants for file validation and storage."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

INPUTS_DIR = DATA_DIR / "inputs"
OUTPUTS_DIR = DATA_DIR / "outputs"
PREVIEWS_DIR = DATA_DIR / "previews"
TEMP_DIR = DATA_DIR / "temp"
JOB_RECORDS_DIR = DATA_DIR / "job_records"

IMAGE_INPUT_DIR = INPUTS_DIR / "images"
VIDEO_INPUT_DIR = INPUTS_DIR / "videos"
SIGNAL_INPUT_DIR = INPUTS_DIR / "signals"
AERIAL_INPUT_DIR = INPUTS_DIR / "aerial"

IMAGE_OUTPUT_DIR = OUTPUTS_DIR / "images"
VIDEO_OUTPUT_DIR = OUTPUTS_DIR / "videos"
SIGNAL_OUTPUT_DIR = OUTPUTS_DIR / "signals"
AERIAL_OUTPUT_DIR = OUTPUTS_DIR / "aerial"

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov"}
ALLOWED_SIGNAL_EXTENSIONS = {".csv"}

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
MAX_AERIAL_SIZE_BYTES = 20 * 1024 * 1024
MAX_VIDEO_SIZE_BYTES = 200 * 1024 * 1024
MAX_SIGNAL_SIZE_BYTES = 10 * 1024 * 1024

FILE_CATEGORY_TO_INPUT_DIR = {
    "image": IMAGE_INPUT_DIR,
    "video": VIDEO_INPUT_DIR,
    "signal": SIGNAL_INPUT_DIR,
    "aerial": AERIAL_INPUT_DIR,
}

FILE_CATEGORY_TO_ALLOWED_EXTENSIONS = {
    "image": ALLOWED_IMAGE_EXTENSIONS,
    "video": ALLOWED_VIDEO_EXTENSIONS,
    "signal": ALLOWED_SIGNAL_EXTENSIONS,
    "aerial": ALLOWED_IMAGE_EXTENSIONS,
}

FILE_CATEGORY_TO_MAX_SIZE = {
    "image": MAX_IMAGE_SIZE_BYTES,
    "video": MAX_VIDEO_SIZE_BYTES,
    "signal": MAX_SIGNAL_SIZE_BYTES,
    "aerial": MAX_AERIAL_SIZE_BYTES,
}

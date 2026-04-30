# SensorVision Workbench

SensorVision Workbench is a full-stack local web application for image enhancement, signal analysis, video object tracking, and aerial image analysis.

## Features

- Secure local file upload handling
- Image enhancement with OpenCV filters
- Signal analysis with smoothing and FFT
- Video object detection and tracking with YOLO
- Aerial image object detection with YOLO
- Dashboard summary and results history
- React frontend with FastAPI backend
- Docker Compose support

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Axios
- React Router

### Backend
- FastAPI
- OpenCV
- NumPy
- SciPy
- pandas
- matplotlib
- Ultralytics YOLO

## Project Structure

```text
sensorvision-workbench/
├── backend/
├── frontend/
├── docs/
├── scripts/
├── docker-compose.yml
└── README.md

Local Development

Backend

cd backend
source .venv/bin/activate
uvicorn app.main:app --reload

Backend runs at:

http://127.0.0.1:8000

API docs:

http://127.0.0.1:8000/docs
Frontend
cd frontend
npm run dev

Frontend runs at:

http://localhost:5173
Docker

Build and run both services:

docker compose up --build

Stop services:

docker compose down


Security Notes

The backend includes a secure file ingestion layer with:

allowed file extension checks
file size limits
UUID-based filenames
sanitized filenames
controlled local storage directories
protected file serving paths
Core Workflows
Image Enhancement

Upload an image and apply Gaussian, Median, or Bilateral filtering.

Signal Analysis

Upload a CSV signal, select a numeric column, smooth the signal, and run FFT frequency analysis.

Video Tracking

Upload a video and run YOLO object detection and tracking.

Aerial Analysis

Upload an aerial-style image and run YOLO-based object detection.

Portfolio Summary

This project demonstrates:

full-stack engineering
API design
computer vision
signal processing
object detection/tracking
secure file handling
local deployment

---

# 7. Test Docker build

Stop any running backend/frontend first:

```bash
pkill -f uvicorn

Then from project root:

docker compose up --build

Open:

http://localhost:5173

And:

http://127.0.0.1:8000/docs

Stop Docker when done:

Ctrl + C
docker compose down

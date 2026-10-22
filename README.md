# SensorVision Workbench

**Full-stack computer-vision and signal-analysis workbench — Python / FastAPI / React / TypeScript**

SensorVision is a locally run engineering workbench for uploading data, executing analysis workflows, reviewing outputs, and inspecting job history. The emphasis is on **modular API design, controlled file handling, repeatable development environments, and computational workflows**, not a hosted SaaS product.

## Capabilities

| Workflow | Implementation |
| --- | --- |
| Image enhancement | OpenCV Gaussian, median, and bilateral filtering |
| Signal analysis | CSV ingestion, smoothing, FFT-based frequency analysis |
| Video processing | YOLO object detection and tracking (including ByteTrack / BoT-SORT options) |
| Aerial image analysis | YOLO object detection on still imagery |
| Results dashboard | Job counts, recent activity, processing history, JSON export |
| File handling | Extension and size checks, sanitized names, UUID-based storage, controlled file access |

## Architecture

This diagram describes the **current local/Docker architecture**. It does not imply cloud deployment or external managed storage.

~~~mermaid
flowchart LR
    U["User / browser"] --> UI["React + TypeScript<br/>Vite frontend :5173"]
    UI -->|"REST / JSON + file uploads"| API["FastAPI :8000<br/>API route + schema layer"]
    API --> VAL["File validation & storage service"]
    API --> PROC["Processing services"]
    PROC --> CV["OpenCV / NumPy / SciPy"]
    PROC --> YOLO["Ultralytics YOLO<br/>detection & tracking"]
    VAL --> FS[("Local data/inputs")]
    PROC --> OUT[("Local data/outputs")]
    PROC --> HIST[("JSON job records")]
    API --> HIST
    HIST -->|"Job list / dashboard / export"| API
    API -->|"Results + file URLs"| UI
~~~

### Engineering boundaries

- **frontend/src/pages/** — dashboard, analysis workflows, job history, and settings.
- **frontend/src/api/** — Axios clients and typed API calls.
- **backend/app/api/routes/** — HTTP request/response routes.
- **backend/app/schemas/** — Pydantic input/output contracts.
- **backend/app/services/** — file validation, processing, model access, job history, and storage operations.
- **backend/app/core/constants.py** — file categories, accepted extensions, maximum upload sizes, and storage directories.
- **backend/data/** — local input/output files and job-record JSON. This is **not** a production database.
- **docker-compose.yml** — local orchestration for backend and frontend development.

## Quick start: Docker Compose

### Prerequisites

- Docker Engine/Desktop with the Compose plugin.
- Enough disk space for the Python, PyTorch CPU, and image-processing dependencies. The initial image build can be substantial.

~~~bash
git clone https://github.com/NamesteSensei/sensorvision-workbench.git
cd sensorvision-workbench
docker compose up --build
~~~

Open:

- **Frontend:** http://localhost:5173
- **FastAPI docs:** http://localhost:8000/docs
- **Backend health:** http://localhost:8000/api/v1/health

The Compose configuration exposes frontend port **5173** and backend port **8000**. The browser connects to the backend through **http://127.0.0.1:8000**, the frontend client's default API URL. Job files persist under the host's **backend/data/** mount.

~~~bash
docker compose down
~~~

**Note:** The frontend container runs the Vite development server. This Compose configuration is intended for **local development**, not internet-facing production hosting.

## Run locally without Docker

### Backend — Python 3.11

~~~bash
cd sensorvision-workbench/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
~~~

On Windows PowerShell, use **py -3.11 -m venv .venv**, then **.venv\Scripts\Activate.ps1** and **Copy-Item .env.example .env**. Install a supported PyTorch version for your system if the default pip resolution is unsuitable. Video/model processing can be resource-intensive.

The example backend environment defines **APP_NAME**, **APP_VERSION**, and **FRONTEND_ORIGIN=http://localhost:5173**.

### Frontend — Node.js 20+

In a separate terminal:

~~~bash
cd sensorvision-workbench/frontend
npm ci
npm run dev
~~~

Open **http://localhost:5173**. The frontend uses **VITE_API_BASE_URL** when provided; otherwise it defaults to **http://127.0.0.1:8000** (see **frontend/src/api/axiosClient.ts**).

The Python API and the Node development server must both be running.

## Try the workflows

1. **Image Processing:** upload a supported image and select an OpenCV filter.
2. **Signal Analysis:** upload a CSV file, choose a numeric column, smoothing window, and sampling frequency. A sample input is available at **backend/test_signal.csv**.
3. **Video Tracking:** upload an MP4/AVI/MOV file and choose the YOLO model and tracking options. Some models may require an initial download.
4. **Aerial Analysis:** upload a still image for YOLO object detection.
5. **Results History:** review stored job records, download available outputs, or export the history as JSON.

The default file size limits and accepted types are defined in **backend/app/core/constants.py** (for example, images 10 MiB, aerial images 20 MiB, videos 200 MiB, CSV signals 10 MiB).

## Key API routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | /api/v1/health | Service health |
| POST | /api/v1/uploads/{file_category} | Validated file upload |
| POST | /api/v1/image-processing/enhance | Apply an image filter |
| POST | /api/v1/signal-analysis/analyze | Analyze CSV signals |
| POST | /api/v1/video-tracking/track | YOLO tracking workflow |
| GET | /api/v1/jobs | List recorded jobs |
| GET | /api/v1/jobs/dashboard | Dashboard summary |
| GET | /api/v1/jobs/export | Export job history |
| GET | /api/v1/files/{file_path} | Serve locally stored output files |

Additional routes are documented in FastAPI's **/docs**.

## Quality checks and project status

~~~bash
# From the frontend directory
npm run lint
npm run build
~~~

These commands are the configured frontend lint/build checks, **not evidence of a passing CI suite**. The repository does not currently include a dedicated automated backend test suite. Review processing behavior and file access controls before relying on the application for sensitive files.

### Security and operational notes

- Uploaded files are stored on the **local filesystem**, not in a managed cloud storage service.
- The current API has **no user authentication**. Run it on trusted local networks; add authentication, authorization, quotas, isolation, and operational controls before exposing it publicly.
- Validation includes allowed types, maximum file sizes, sanitized stored names, and generated identifiers. This is **defense-in-depth**, not a guarantee that every hostile file is safe.
- Video tracking uses computationally expensive models; workloads may take time and consume substantial RAM/CPU.
- Stored job history is JSON on disk and will not automatically synchronize across multiple instances.
- Generated data in **backend/data/** should not be committed; check for sensitive content before sharing examples.

## Engineering considerations

The architectural tradeoff is deliberate: a lightweight React client talks to typed FastAPI endpoints, computational services remain separate from route handlers, and file/job persistence is straightforward to inspect locally. Next improvements could include automated tests, background job execution, metrics/benchmark harnesses, stronger file-path containment, authentication, and deployment hardening.

## License

No open-source license file is currently provided; public repository visibility does not automatically grant reuse rights.
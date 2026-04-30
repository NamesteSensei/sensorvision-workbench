import { useState } from "react";

import { trackVideo } from "../api/videoTrackingApi";
import type {
  TrackerName,
  VideoTrackingResponse,
} from "../types/videoTrackingTypes";
import { buildBackendFileUrl } from "../utils/fileUrlHelpers";

export default function VideoTrackingPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [modelName, setModelName] = useState<string>("yolov8n.pt");
  const [trackerName, setTrackerName] = useState<TrackerName>("bytetrack.yaml");
  const [confidenceThreshold, setConfidenceThreshold] = useState<number>(0.25);
  const [iouThreshold, setIouThreshold] = useState<number>(0.45);
  const [result, setResult] = useState<VideoTrackingResponse | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isTracking, setIsTracking] = useState<boolean>(false);

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
    setResult(null);
    setErrorMessage("");
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setErrorMessage("Please select a video file first.");
      return;
    }

    setIsTracking(true);
    setErrorMessage("");
    setResult(null);

    try {
      const response = await trackVideo({
        videoFile: selectedFile,
        modelName,
        trackerName,
        confidenceThreshold,
        iouThreshold,
      });

      setResult(response);
    } catch (error) {
      setErrorMessage("Video tracking failed. Check the backend logs.");
    } finally {
      setIsTracking(false);
    }
  }

  return (
    <div>
      <h1>Video Detection & Tracking</h1>
      <p>
        Upload a video, run YOLO object detection and tracking, then review the
        annotated output video and tracking metrics.
      </p>

      <form onSubmit={handleSubmit} style={{ marginTop: "1rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="video-file">Video File</label>
          <br />
          <input
            id="video-file"
            type="file"
            accept=".mp4,.avi,.mov"
            onChange={handleFileChange}
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="model-name">YOLO Model</label>
          <br />
          <select
            id="model-name"
            value={modelName}
            onChange={(event) => setModelName(event.target.value)}
          >
            <option value="yolov8n.pt">YOLOv8 Nano</option>
            <option value="yolov8s.pt">YOLOv8 Small</option>
          </select>
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="tracker-name">Tracker</label>
          <br />
          <select
            id="tracker-name"
            value={trackerName}
            onChange={(event) =>
              setTrackerName(event.target.value as TrackerName)
            }
          >
            <option value="bytetrack.yaml">ByteTrack</option>
            <option value="botsort.yaml">BoT-SORT</option>
          </select>
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="confidence-threshold">
            Confidence Threshold: {confidenceThreshold}
          </label>
          <br />
          <input
            id="confidence-threshold"
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={confidenceThreshold}
            onChange={(event) =>
              setConfidenceThreshold(Number(event.target.value))
            }
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="iou-threshold">IoU Threshold: {iouThreshold}</label>
          <br />
          <input
            id="iou-threshold"
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={iouThreshold}
            onChange={(event) => setIouThreshold(Number(event.target.value))}
          />
        </div>

        <button type="submit" disabled={isTracking}>
          {isTracking ? "Tracking video..." : "Run Tracking"}
        </button>
      </form>

      {errorMessage && (
        <p style={{ color: "red", marginTop: "1rem" }}>{errorMessage}</p>
      )}

      {previewUrl && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Original Video Preview</h2>
          <video
            src={previewUrl}
            controls
            style={{
              maxWidth: "720px",
              width: "100%",
              border: "1px solid #ddd",
            }}
          />
        </div>
      )}

      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Tracking Results</h2>

          <div style={{ marginBottom: "1rem" }}>
            <p>
              <strong>Original File:</strong> {result.original_file_name}
            </p>
            <p>
              <strong>Processed File:</strong> {result.processed_file_name}
            </p>
            <p>
              <strong>Model:</strong> {result.model_name}
            </p>
            <p>
              <strong>Tracker:</strong> {result.tracker_name}
            </p>
            <p>
              <strong>Frames:</strong> {result.frame_count}
            </p>
            <p>
              <strong>FPS:</strong> {result.fps}
            </p>
            <p>
              <strong>Unique Tracks:</strong> {result.unique_track_count}
            </p>
            <p>
              <strong>File Size:</strong> {result.file_size_bytes} bytes
            </p>
          </div>

          <h3>Class Counts</h3>
          {Object.keys(result.class_counts).length === 0 ? (
            <p>No objects detected.</p>
          ) : (
            <table
              style={{
                borderCollapse: "collapse",
                marginBottom: "1.5rem",
                minWidth: "260px",
              }}
            >
              <thead>
                <tr>
                  <th style={{ border: "1px solid #ddd", padding: "0.5rem" }}>
                    Class
                  </th>
                  <th style={{ border: "1px solid #ddd", padding: "0.5rem" }}>
                    Count
                  </th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(result.class_counts).map(
                  ([className, count]) => (
                    <tr key={className}>
                      <td
                        style={{
                          border: "1px solid #ddd",
                          padding: "0.5rem",
                        }}
                      >
                        {className}
                      </td>
                      <td
                        style={{
                          border: "1px solid #ddd",
                          padding: "0.5rem",
                        }}
                      >
                        {count}
                      </td>
                    </tr>
                  ),
                )}
              </tbody>
            </table>
          )}

          <h3>Processed Video</h3>
          <video
            src={buildBackendFileUrl(result.processed_video_url)}
            controls
            style={{
              maxWidth: "720px",
              width: "100%",
              border: "1px solid #ddd",
            }}
          />

          <div style={{ marginTop: "1rem" }}>
            <a
              href={buildBackendFileUrl(result.processed_video_url)}
              target="_blank"
              rel="noreferrer"
            >
              Open processed video
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

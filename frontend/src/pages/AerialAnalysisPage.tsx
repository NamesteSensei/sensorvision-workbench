import { useState } from "react";

import { analyzeAerialImage } from "../api/aerialAnalysisApi";
import type { AerialAnalysisResponse } from "../types/aerialAnalysisTypes";
import { buildBackendFileUrl } from "../utils/fileUrlHelpers";

export default function AerialAnalysisPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [modelName, setModelName] = useState<string>("yolov8n.pt");
  const [confidenceThreshold, setConfidenceThreshold] = useState<number>(0.25);
  const [iouThreshold, setIouThreshold] = useState<number>(0.45);
  const [result, setResult] = useState<AerialAnalysisResponse | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

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
      setErrorMessage("Please select an aerial image first.");
      return;
    }

    setIsAnalyzing(true);
    setErrorMessage("");
    setResult(null);

    try {
      const response = await analyzeAerialImage({
        imageFile: selectedFile,
        modelName,
        confidenceThreshold,
        iouThreshold,
      });

      setResult(response);
    } catch (error) {
      setErrorMessage("Aerial analysis failed. Check the backend logs.");
    } finally {
      setIsAnalyzing(false);
    }
  }

  return (
    <div>
      <h1>Aerial Image Analysis</h1>
      <p>
        Upload an aerial or satellite-style image and run YOLO-based object
        detection to generate an annotated result image and class summary.
      </p>

      <form onSubmit={handleSubmit} style={{ marginTop: "1rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="aerial-file">Aerial Image File</label>
          <br />
          <input
            id="aerial-file"
            type="file"
            accept=".jpg,.jpeg,.png,.bmp,.tif,.tiff"
            onChange={handleFileChange}
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="aerial-model-name">YOLO Model</label>
          <br />
          <select
            id="aerial-model-name"
            value={modelName}
            onChange={(event) => setModelName(event.target.value)}
          >
            <option value="yolov8n.pt">YOLOv8 Nano</option>
            <option value="yolov8s.pt">YOLOv8 Small</option>
          </select>
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="aerial-confidence-threshold">
            Confidence Threshold: {confidenceThreshold}
          </label>
          <br />
          <input
            id="aerial-confidence-threshold"
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
          <label htmlFor="aerial-iou-threshold">
            IoU Threshold: {iouThreshold}
          </label>
          <br />
          <input
            id="aerial-iou-threshold"
            type="range"
            min="0"
            max="1"
            step="0.05"
            value={iouThreshold}
            onChange={(event) => setIouThreshold(Number(event.target.value))}
          />
        </div>

        <button type="submit" disabled={isAnalyzing}>
          {isAnalyzing ? "Analyzing image..." : "Analyze Aerial Image"}
        </button>
      </form>

      {errorMessage && (
        <p style={{ color: "red", marginTop: "1rem" }}>{errorMessage}</p>
      )}

      <div
        style={{
          display: "flex",
          gap: "2rem",
          marginTop: "2rem",
          alignItems: "flex-start",
          flexWrap: "wrap",
        }}
      >
        {previewUrl && (
          <div>
            <h2>Original Image</h2>
            <img
              src={previewUrl}
              alt="Original aerial upload preview"
              style={{ maxWidth: "480px", border: "1px solid #ddd" }}
            />
          </div>
        )}

        {result && (
          <div>
            <h2>Annotated Result</h2>
            <img
              src={buildBackendFileUrl(result.processed_image_url)}
              alt="Processed aerial detection result"
              style={{ maxWidth: "480px", border: "1px solid #ddd" }}
            />

            <div style={{ marginTop: "1rem" }}>
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
                <strong>Detected Objects:</strong>{" "}
                {result.detected_object_count}
              </p>
              <p>
                <strong>File Size:</strong> {result.file_size_bytes} bytes
              </p>

              <h3>Class Counts</h3>
              {Object.keys(result.class_counts).length === 0 ? (
                <p>No objects detected.</p>
              ) : (
                <table
                  style={{
                    borderCollapse: "collapse",
                    marginBottom: "1rem",
                    minWidth: "260px",
                  }}
                >
                  <thead>
                    <tr>
                      <th
                        style={{
                          border: "1px solid #ddd",
                          padding: "0.5rem",
                        }}
                      >
                        Class
                      </th>
                      <th
                        style={{
                          border: "1px solid #ddd",
                          padding: "0.5rem",
                        }}
                      >
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

              <a
                href={buildBackendFileUrl(result.processed_image_url)}
                target="_blank"
                rel="noreferrer"
              >
                Open annotated image
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

import { useState } from "react";

import { processImage } from "../api/imageProcessingApi";
import type {
  ImageFilterName,
  ImageProcessingResponse,
} from "../types/imageProcessingTypes";
import { buildBackendFileUrl } from "../utils/fileUrlHelpers";

export default function ImageProcessingPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [filterName, setFilterName] = useState<ImageFilterName>("gaussian");
  const [kernelSize, setKernelSize] = useState<number>(5);
  const [sigmaValue, setSigmaValue] = useState<number>(1.0);
  const [result, setResult] = useState<ImageProcessingResponse | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isProcessing, setIsProcessing] = useState<boolean>(false);

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
      setErrorMessage("Please select an image file first.");
      return;
    }

    setIsProcessing(true);
    setErrorMessage("");
    setResult(null);

    try {
      const response = await processImage({
        imageFile: selectedFile,
        filterName,
        kernelSize,
        sigmaValue,
      });

      setResult(response);
    } catch (error) {
      setErrorMessage("Image processing failed. Check the backend logs.");
    } finally {
      setIsProcessing(false);
    }
  }

  return (
    <div>
      <h1>Image Enhancement</h1>
      <p>
        Upload an image and apply Gaussian, Median, or Bilateral filtering.
      </p>

      <form onSubmit={handleSubmit} style={{ marginTop: "1rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="image-file">Image File</label>
          <br />
          <input
            id="image-file"
            type="file"
            accept=".jpg,.jpeg,.png,.bmp,.tif,.tiff"
            onChange={handleFileChange}
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="filter-name">Filter</label>
          <br />
          <select
            id="filter-name"
            value={filterName}
            onChange={(event) =>
              setFilterName(event.target.value as ImageFilterName)
            }
          >
            <option value="gaussian">Gaussian Blur</option>
            <option value="median">Median Blur</option>
            <option value="bilateral">Bilateral Filter</option>
          </select>
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="kernel-size">Kernel Size</label>
          <br />
          <input
            id="kernel-size"
            type="number"
            min="3"
            max="31"
            step="2"
            value={kernelSize}
            onChange={(event) => setKernelSize(Number(event.target.value))}
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="sigma-value">Sigma Value</label>
          <br />
          <input
            id="sigma-value"
            type="number"
            min="0"
            max="10"
            step="0.5"
            value={sigmaValue}
            onChange={(event) => setSigmaValue(Number(event.target.value))}
          />
        </div>

        <button type="submit" disabled={isProcessing}>
          {isProcessing ? "Processing..." : "Process Image"}
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
        }}
      >
        {previewUrl && (
          <div>
            <h2>Original Image</h2>
            <img
              src={previewUrl}
              alt="Original upload preview"
              style={{ maxWidth: "400px", border: "1px solid #ddd" }}
            />
          </div>
        )}

        {result && (
          <div>
            <h2>Processed Image</h2>
            <img
              src={buildBackendFileUrl(result.processed_image_url)}
              alt="Processed result"
              style={{ maxWidth: "400px", border: "1px solid #ddd" }}
            />

            <div style={{ marginTop: "1rem" }}>
              <p>
                <strong>Filter:</strong> {result.filter_name}
              </p>
              <p>
                <strong>Original File:</strong> {result.original_file_name}
              </p>
              <p>
                <strong>Processed File:</strong> {result.processed_file_name}
              </p>
              <p>
                <strong>File Size:</strong> {result.file_size_bytes} bytes
              </p>

              <a
                href={buildBackendFileUrl(result.processed_image_url)}
                target="_blank"
                rel="noreferrer"
              >
                Open processed image
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

import { useState } from "react";

import { analyzeSignal } from "../api/signalAnalysisApi";
import type { SignalAnalysisResponse } from "../types/signalAnalysisTypes";
import { buildBackendFileUrl } from "../utils/fileUrlHelpers";

export default function SignalAnalysisPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedColumn, setSelectedColumn] = useState<string>("value");
  const [samplingRateHz, setSamplingRateHz] = useState<number>(20);
  const [smoothingWindow, setSmoothingWindow] = useState<number>(5);
  const [result, setResult] = useState<SignalAnalysisResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setSelectedFile(file);
    setResult(null);
    setErrorMessage("");
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setErrorMessage("Please select a CSV file first.");
      return;
    }

    setIsAnalyzing(true);
    setErrorMessage("");
    setResult(null);

    try {
      const response = await analyzeSignal({
        signalFile: selectedFile,
        selectedColumn,
        samplingRateHz,
        smoothingWindow,
      });

      setResult(response);
    } catch (error) {
      setErrorMessage("Signal analysis failed. Check the CSV and backend logs.");
    } finally {
      setIsAnalyzing(false);
    }
  }

  return (
    <div>
      <h1>Signal Analysis</h1>
      <p>
        Upload a CSV file, select a numeric column, smooth the signal, and
        analyze its frequency content with FFT.
      </p>

      <form onSubmit={handleSubmit} style={{ marginTop: "1rem" }}>
        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="signal-file">CSV File</label>
          <br />
          <input
            id="signal-file"
            type="file"
            accept=".csv"
            onChange={handleFileChange}
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="selected-column">Signal Column Name</label>
          <br />
          <input
            id="selected-column"
            type="text"
            value={selectedColumn}
            onChange={(event) => setSelectedColumn(event.target.value)}
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="sampling-rate">Sampling Rate Hz</label>
          <br />
          <input
            id="sampling-rate"
            type="number"
            min="0.1"
            step="0.1"
            value={samplingRateHz}
            onChange={(event) =>
              setSamplingRateHz(Number(event.target.value))
            }
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label htmlFor="smoothing-window">Smoothing Window</label>
          <br />
          <input
            id="smoothing-window"
            type="number"
            min="1"
            max="501"
            step="2"
            value={smoothingWindow}
            onChange={(event) =>
              setSmoothingWindow(Number(event.target.value))
            }
          />
        </div>

        <button type="submit" disabled={isAnalyzing}>
          {isAnalyzing ? "Analyzing..." : "Analyze Signal"}
        </button>
      </form>

      {errorMessage && (
        <p style={{ color: "red", marginTop: "1rem" }}>{errorMessage}</p>
      )}

      {result && (
        <div style={{ marginTop: "2rem" }}>
          <h2>Analysis Results</h2>

          <div style={{ marginBottom: "1rem" }}>
            <p>
              <strong>Original File:</strong> {result.original_file_name}
            </p>
            <p>
              <strong>Selected Column:</strong> {result.selected_column}
            </p>
            <p>
              <strong>Sample Count:</strong> {result.sample_count}
            </p>
            <p>
              <strong>Sampling Rate:</strong> {result.sampling_rate_hz} Hz
            </p>
            <p>
              <strong>Smoothing Window:</strong> {result.smoothing_window}
            </p>
            <p>
              <strong>File Size:</strong> {result.file_size_bytes} bytes
            </p>
          </div>

          <div style={{ marginBottom: "2rem" }}>
            <h3>Time Domain Plot</h3>
            <img
              src={buildBackendFileUrl(result.time_plot_url)}
              alt="Time domain signal plot"
              style={{ maxWidth: "100%", border: "1px solid #ddd" }}
            />
          </div>

          <div style={{ marginBottom: "2rem" }}>
            <h3>Frequency Domain Plot</h3>
            <img
              src={buildBackendFileUrl(result.frequency_plot_url)}
              alt="Frequency domain magnitude plot"
              style={{ maxWidth: "100%", border: "1px solid #ddd" }}
            />
          </div>

          <div>
            <a
              href={buildBackendFileUrl(result.time_plot_url)}
              target="_blank"
              rel="noreferrer"
            >
              Open time-domain plot
            </a>
            <br />
            <a
              href={buildBackendFileUrl(result.frequency_plot_url)}
              target="_blank"
              rel="noreferrer"
            >
              Open frequency-domain plot
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

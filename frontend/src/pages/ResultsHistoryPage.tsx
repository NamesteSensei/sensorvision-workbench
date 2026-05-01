import { useEffect, useState } from "react";

import {
  exportJobHistory,
  getJobHistory,
  resetJobHistory,
} from "../api/jobHistoryApi";
import type { JobHistoryRecord } from "../types/jobHistoryTypes";
import { buildBackendFileUrl } from "../utils/fileUrlHelpers";

export default function ResultsHistoryPage() {
  const [jobs, setJobs] = useState<JobHistoryRecord[]>([]);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(true);

  async function loadJobHistory() {
    setIsLoading(true);
    setErrorMessage("");

    try {
      const response = await getJobHistory();
      setJobs(response.jobs);
    } catch (error) {
      setErrorMessage("Could not load job history.");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleResetHistory() {
    const shouldReset = window.confirm(
      "Are you sure you want to clear all job history records?",
    );

    if (!shouldReset) {
      return;
    }

    try {
      await resetJobHistory();
      await loadJobHistory();
    } catch (error) {
      setErrorMessage("Could not reset job history.");
    }
  }

  async function handleExportHistory() {
    try {
      const historyExport = await exportJobHistory();
      const blob = new Blob([JSON.stringify(historyExport, null, 2)], {
        type: "application/json",
      });

      const downloadUrl = URL.createObjectURL(blob);
      const link = document.createElement("a");

      link.href = downloadUrl;
      link.download = "sensorvision-job-history.json";
      link.click();

      URL.revokeObjectURL(downloadUrl);
    } catch (error) {
      setErrorMessage("Could not export job history.");
    }
  }

  useEffect(() => {
    loadJobHistory();
  }, []);

  return (
    <div>
      <h1>Results History</h1>
      <p>
        Review previously processed images, signals, videos, and aerial analysis
        outputs.
      </p>

      <div style={{ display: "flex", gap: "1rem", marginTop: "1rem" }}>
        <button type="button" onClick={loadJobHistory}>
          Reload History
        </button>

        <button type="button" onClick={handleExportHistory}>
          Export History JSON
        </button>

        <button type="button" onClick={handleResetHistory}>
          Reset Dashboard
        </button>
      </div>

      {errorMessage && (
        <p style={{ color: "red", marginTop: "1rem" }}>{errorMessage}</p>
      )}

      {isLoading ? (
        <p>Loading results history...</p>
      ) : jobs.length === 0 ? (
        <p>No results have been saved yet.</p>
      ) : (
        <table className="data-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Input File</th>
              <th>Output File</th>
              <th>Created</th>
              <th>Output</th>
              <th>Summary</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.job_id}>
                <td>{job.job_type}</td>
                <td>{job.original_file_name}</td>
                <td>{job.output_file_name}</td>
                <td>{new Date(job.created_at).toLocaleString()}</td>
                <td>
                  <a
                    href={buildBackendFileUrl(job.output_url)}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Open
                  </a>
                </td>
                <td>
                  <pre className="summary-preview">
                    {JSON.stringify(job.summary, null, 2)}
                  </pre>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

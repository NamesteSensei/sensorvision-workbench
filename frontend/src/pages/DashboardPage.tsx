import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getDashboardSummary } from "../api/jobHistoryApi";
import type { DashboardSummaryResponse } from "../types/jobHistoryTypes";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummaryResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    async function loadDashboardSummary() {
      try {
        const response = await getDashboardSummary();
        setSummary(response);
      } catch (error) {
        setErrorMessage("Could not load dashboard summary.");
      }
    }

    loadDashboardSummary();
  }, []);

  return (
    <div>
      <h1>SensorVision Dashboard</h1>
      <p>
        Monitor processing activity across image enhancement, signal analysis,
        video tracking, and aerial analysis workflows.
      </p>

      {errorMessage && (
        <p style={{ color: "red", marginTop: "1rem" }}>{errorMessage}</p>
      )}

      {!summary ? (
        <p>Loading dashboard...</p>
      ) : (
        <>
          <div className="metric-grid">
            <div className="metric-card">
              <h3>Total Jobs</h3>
              <p>{summary.total_jobs}</p>
            </div>

            <div className="metric-card">
              <h3>Image Jobs</h3>
              <p>{summary.image_jobs}</p>
            </div>

            <div className="metric-card">
              <h3>Signal Jobs</h3>
              <p>{summary.signal_jobs}</p>
            </div>

            <div className="metric-card">
              <h3>Video Jobs</h3>
              <p>{summary.video_jobs}</p>
            </div>

            <div className="metric-card">
              <h3>Aerial Jobs</h3>
              <p>{summary.aerial_jobs}</p>
            </div>
          </div>

          <div style={{ marginTop: "2rem" }}>
            <h2>Recent Jobs</h2>

            {summary.recent_jobs.length === 0 ? (
              <p>No jobs have been recorded yet.</p>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Type</th>
                    <th>Input File</th>
                    <th>Output File</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {summary.recent_jobs.map((job) => (
                    <tr key={job.job_id}>
                      <td>{job.job_type}</td>
                      <td>{job.original_file_name}</td>
                      <td>{job.output_file_name}</td>
                      <td>{new Date(job.created_at).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}

            <p style={{ marginTop: "1rem" }}>
              <Link to="/results-history">View all results</Link>
            </p>
          </div>
        </>
      )}
    </div>
  );
}

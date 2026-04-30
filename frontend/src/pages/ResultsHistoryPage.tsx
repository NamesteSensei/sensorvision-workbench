import { useEffect, useState } from "react";

import { getJobHistory } from "../api/jobHistoryApi";
import type { JobHistoryRecord } from "../types/jobHistoryTypes";
import { buildBackendFileUrl } from "../utils/fileUrlHelpers";

export default function ResultsHistoryPage() {
  const [jobs, setJobs] = useState<JobHistoryRecord[]>([]);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    async function loadJobHistory() {
      try {
        const response = await getJobHistory();
        setJobs(response.jobs);
      } catch (error) {
        setErrorMessage("Could not load job history.");
      } finally {
        setIsLoading(false);
      }
    }

    loadJobHistory();
  }, []);

  return (
    <div>
      <h1>Results History</h1>
      <p>
        Review previously processed images, signals, videos, and aerial analysis
        outputs.
      </p>

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

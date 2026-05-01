import { useEffect, useState } from "react";

import { getSystemInfo } from "../api/systemInfoApi";
import type { SystemInfoResponse } from "../types/systemInfoTypes";

export default function SettingsPage() {
  const [systemInfo, setSystemInfo] = useState<SystemInfoResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  useEffect(() => {
    async function loadSystemInfo() {
      try {
        const response = await getSystemInfo();
        setSystemInfo(response);
      } catch (error) {
        setErrorMessage("Could not load system settings.");
      }
    }

    loadSystemInfo();
  }, []);

  return (
    <div>
      <h1>Settings & System Status</h1>
      <p>
        Review backend health, storage configuration, upload limits, model
        options, and security controls.
      </p>

      {errorMessage && (
        <p style={{ color: "red", marginTop: "1rem" }}>{errorMessage}</p>
      )}

      {!systemInfo ? (
        <p>Loading settings...</p>
      ) : (
        <>
          <div className="metric-grid">
            <div className="metric-card">
              <h3>API Status</h3>
              <p>{systemInfo.api_status}</p>
            </div>

            <div className="metric-card">
              <h3>App Version</h3>
              <p>{systemInfo.app_version}</p>
            </div>

            <div className="metric-card">
              <h3>Storage</h3>
              <p>{systemInfo.storage_mode}</p>
            </div>

            <div className="metric-card">
              <h3>Default Model</h3>
              <p>{systemInfo.default_yolo_model}</p>
            </div>
          </div>

          <section style={{ marginTop: "2rem" }}>
            <h2>Application</h2>
            <table className="data-table">
              <tbody>
                <tr>
                  <th>Application Name</th>
                  <td>{systemInfo.app_name}</td>
                </tr>
                <tr>
                  <th>API Docs</th>
                  <td>
                    <a
                      href={systemInfo.api_docs_url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      Open API Docs
                    </a>
                  </td>
                </tr>
              </tbody>
            </table>
          </section>

          <section style={{ marginTop: "2rem" }}>
            <h2>Upload Limits</h2>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Max Size MB</th>
                  <th>Allowed Extensions</th>
                </tr>
              </thead>
              <tbody>
                {systemInfo.upload_limits.map((limit) => (
                  <tr key={limit.category}>
                    <td>{limit.category}</td>
                    <td>{limit.max_size_mb}</td>
                    <td>{limit.allowed_extensions.join(", ")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          <section style={{ marginTop: "2rem" }}>
            <h2>Model Options</h2>
            <table className="data-table">
              <tbody>
                <tr>
                  <th>Supported YOLO Models</th>
                  <td>{systemInfo.supported_yolo_models.join(", ")}</td>
                </tr>
                <tr>
                  <th>Supported Trackers</th>
                  <td>{systemInfo.supported_trackers.join(", ")}</td>
                </tr>
              </tbody>
            </table>
          </section>

          <section style={{ marginTop: "2rem" }}>
            <h2>Security Features</h2>
            <ul>
              {systemInfo.security_features.map((feature) => (
                <li key={feature}>{feature}</li>
              ))}
            </ul>
          </section>
        </>
      )}
    </div>
  );
}

import { Link, Outlet } from "react-router-dom";

export default function AppShell() {
  return (
    <div style={{ display: "flex", minHeight: "100vh" }}>
      <aside
        style={{
          width: "240px",
          padding: "1rem",
          borderRight: "1px solid #ddd",
        }}
      >
        <h2>SensorVision</h2>
        <nav style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
          <Link to="/">Dashboard</Link>
          <Link to="/image-processing">Image Processing</Link>
          <Link to="/signal-analysis">Signal Analysis</Link>
          <Link to="/video-tracking">Video Tracking</Link>
          <Link to="/aerial-analysis">Aerial Analysis</Link>
          <Link to="/results-history">Results History</Link>
          <Link to="/settings">Settings</Link>
        </nav>
      </aside>

      <main style={{ flex: 1, padding: "1.5rem" }}>
        <Outlet />
      </main>
    </div>
  );
}

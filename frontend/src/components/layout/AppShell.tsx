import { Link, Outlet } from "react-router-dom";

export default function AppShell() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h2>SensorVision</h2>

        <nav className="sidebar-nav">
          <Link to="/">Dashboard</Link>
          <Link to="/image-processing">Image Processing</Link>
          <Link to="/signal-analysis">Signal Analysis</Link>
          <Link to="/video-tracking">Video Tracking</Link>
          <Link to="/aerial-analysis">Aerial Analysis</Link>
          <Link to="/results-history">Results History</Link>
          <Link to="/settings">Settings</Link>
        </nav>
      </aside>

      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}

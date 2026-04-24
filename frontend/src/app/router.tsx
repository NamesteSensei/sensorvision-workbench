import { createBrowserRouter } from "react-router-dom";

import AppShell from "../components/layout/AppShell";
import AerialAnalysisPage from "../pages/AerialAnalysisPage";
import DashboardPage from "../pages/DashboardPage";
import ImageProcessingPage from "../pages/ImageProcessingPage";
import ResultsHistoryPage from "../pages/ResultsHistoryPage";
import SettingsPage from "../pages/SettingsPage";
import SignalAnalysisPage from "../pages/SignalAnalysisPage";
import VideoTrackingPage from "../pages/VideoTrackingPage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      {
        index: true,
        element: <DashboardPage />,
      },
      {
        path: "image-processing",
        element: <ImageProcessingPage />,
      },
      {
        path: "signal-analysis",
        element: <SignalAnalysisPage />,
      },
      {
        path: "video-tracking",
        element: <VideoTrackingPage />,
      },
      {
        path: "aerial-analysis",
        element: <AerialAnalysisPage />,
      },
      {
        path: "results-history",
        element: <ResultsHistoryPage />,
      },
      {
        path: "settings",
        element: <SettingsPage />,
      },
    ],
  },
]);

export default router;

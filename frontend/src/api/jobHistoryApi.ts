import axiosClient from "./axiosClient";
import type {
  DashboardSummaryResponse,
  JobHistoryResponse,
} from "../types/jobHistoryTypes";

export async function getDashboardSummary(): Promise<DashboardSummaryResponse> {
  const response = await axiosClient.get<DashboardSummaryResponse>(
    "/api/v1/jobs/dashboard",
  );

  return response.data;
}

export async function getJobHistory(): Promise<JobHistoryResponse> {
  const response = await axiosClient.get<JobHistoryResponse>("/api/v1/jobs");

  return response.data;
}

export async function resetJobHistory(): Promise<void> {
  await axiosClient.delete("/api/v1/jobs/reset");
}

export async function exportJobHistory(): Promise<Record<string, unknown>> {
  const response = await axiosClient.get<Record<string, unknown>>(
    "/api/v1/jobs/export",
  );

  return response.data;
}

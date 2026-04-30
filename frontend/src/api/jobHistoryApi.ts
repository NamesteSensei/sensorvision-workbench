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

import axiosClient from "./axiosClient";
import type { SystemInfoResponse } from "../types/systemInfoTypes";

export async function getSystemInfo(): Promise<SystemInfoResponse> {
  const response = await axiosClient.get<SystemInfoResponse>("/api/v1/system/info");

  return response.data;
}

import axiosClient from "./axiosClient";
import type { SignalAnalysisResponse } from "../types/signalAnalysisTypes";

interface AnalyzeSignalParams {
  signalFile: File;
  selectedColumn: string;
  samplingRateHz: number;
  smoothingWindow: number;
}

export async function analyzeSignal(
  params: AnalyzeSignalParams,
): Promise<SignalAnalysisResponse> {
  const formData = new FormData();

  formData.append("upload_file", params.signalFile);
  formData.append("selected_column", params.selectedColumn);
  formData.append("sampling_rate_hz", String(params.samplingRateHz));
  formData.append("smoothing_window", String(params.smoothingWindow));

  const response = await axiosClient.post<SignalAnalysisResponse>(
    "/api/v1/signal-analysis/analyze",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  );

  return response.data;
}

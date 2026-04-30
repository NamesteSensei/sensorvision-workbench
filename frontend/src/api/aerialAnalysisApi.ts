import axiosClient from "./axiosClient";
import type { AerialAnalysisResponse } from "../types/aerialAnalysisTypes";

interface AnalyzeAerialImageParams {
  imageFile: File;
  modelName: string;
  confidenceThreshold: number;
  iouThreshold: number;
}

export async function analyzeAerialImage(
  params: AnalyzeAerialImageParams,
): Promise<AerialAnalysisResponse> {
  const formData = new FormData();

  formData.append("upload_file", params.imageFile);
  formData.append("model_name", params.modelName);
  formData.append("confidence_threshold", String(params.confidenceThreshold));
  formData.append("iou_threshold", String(params.iouThreshold));

  const response = await axiosClient.post<AerialAnalysisResponse>(
    "/api/v1/aerial-analysis/analyze",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  );

  return response.data;
}

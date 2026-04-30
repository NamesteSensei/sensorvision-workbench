import axiosClient from "./axiosClient";
import type {
  TrackerName,
  VideoTrackingResponse,
} from "../types/videoTrackingTypes";

interface TrackVideoParams {
  videoFile: File;
  modelName: string;
  trackerName: TrackerName;
  confidenceThreshold: number;
  iouThreshold: number;
}

export async function trackVideo(
  params: TrackVideoParams,
): Promise<VideoTrackingResponse> {
  const formData = new FormData();

  formData.append("upload_file", params.videoFile);
  formData.append("model_name", params.modelName);
  formData.append("tracker_name", params.trackerName);
  formData.append("confidence_threshold", String(params.confidenceThreshold));
  formData.append("iou_threshold", String(params.iouThreshold));

  const response = await axiosClient.post<VideoTrackingResponse>(
    "/api/v1/video-tracking/track",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    },
  );

  return response.data;
}

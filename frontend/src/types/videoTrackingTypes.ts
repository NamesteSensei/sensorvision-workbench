export type TrackerName = "bytetrack.yaml" | "botsort.yaml";

export interface VideoTrackingResponse {
  job_id: string;
  original_file_name: string;
  stored_file_name: string;
  processed_file_name: string;
  file_category: string;
  model_name: string;
  tracker_name: TrackerName;
  confidence_threshold: number;
  frame_count: number;
  fps: number;
  unique_track_count: number;
  class_counts: Record<string, number>;
  processed_video_url: string;
  file_size_bytes: number;
  message: string;
}

export interface AerialAnalysisResponse {
  job_id: string;
  original_file_name: string;
  stored_file_name: string;
  processed_file_name: string;
  file_category: string;
  model_name: string;
  confidence_threshold: number;
  detected_object_count: number;
  class_counts: Record<string, number>;
  processed_image_url: string;
  file_size_bytes: number;
  message: string;
}

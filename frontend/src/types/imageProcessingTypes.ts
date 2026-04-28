export type ImageFilterName = "gaussian" | "median" | "bilateral";

export interface ImageProcessingResponse {
  job_id: string;
  original_file_name: string;
  stored_file_name: string;
  processed_file_name: string;
  file_category: string;
  filter_name: ImageFilterName;
  processed_image_url: string;
  file_size_bytes: number;
  message: string;
}

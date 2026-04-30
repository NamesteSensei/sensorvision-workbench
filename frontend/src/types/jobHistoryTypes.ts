export interface JobHistoryRecord {
  job_id: string;
  job_type: string;
  original_file_name: string;
  output_file_name: string;
  output_url: string;
  created_at: string;
  summary: Record<string, unknown>;
}

export interface JobHistoryResponse {
  jobs: JobHistoryRecord[];
}

export interface DashboardSummaryResponse {
  total_jobs: number;
  image_jobs: number;
  signal_jobs: number;
  video_jobs: number;
  aerial_jobs: number;
  recent_jobs: JobHistoryRecord[];
}

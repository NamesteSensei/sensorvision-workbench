export interface SignalAnalysisResponse {
  job_id: string;
  original_file_name: string;
  stored_file_name: string;
  file_category: string;
  selected_column: string;
  sample_count: number;
  sampling_rate_hz: number;
  smoothing_window: number;
  time_plot_url: string;
  frequency_plot_url: string;
  file_size_bytes: number;
  message: string;
}

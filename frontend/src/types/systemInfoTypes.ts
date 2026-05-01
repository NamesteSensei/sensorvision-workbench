export interface UploadLimit {
  category: string;
  max_size_mb: number;
  allowed_extensions: string[];
}

export interface SystemInfoResponse {
  app_name: string;
  app_version: string;
  api_status: string;
  storage_mode: string;
  api_docs_url: string;
  default_yolo_model: string;
  supported_yolo_models: string[];
  supported_trackers: string[];
  upload_limits: UploadLimit[];
  security_features: string[];
}

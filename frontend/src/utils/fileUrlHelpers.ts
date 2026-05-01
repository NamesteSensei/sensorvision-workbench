const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000";

export function buildBackendFileUrl(fileUrl: string): string {
  return `${API_BASE_URL}/api/v1/files${fileUrl}`;
}

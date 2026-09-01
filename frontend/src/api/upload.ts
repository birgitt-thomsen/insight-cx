import { apiClient } from "./client";

export interface UploadResult {
  imported: number;
  processed: number;
  failed: number;
}

export function uploadFeedbackCsv(file: File) {
  const formData = new FormData();
  formData.append("file", file);
  return apiClient.postForm<UploadResult>("/upload", formData);
}

import { apiClient } from "./client";

export function reanalyzeAllFeedback() {
  return apiClient.post<{ processed: number; failed: number }>(
    "/maintenance/reanalyze-all",
  );
}

export function deleteAllAnalyses() {
  return apiClient.post<{ success: boolean }>("/maintenance/delete-analyses");
}

export function deleteAllFeedback() {
  return apiClient.post<{ success: boolean }>("/maintenance/delete-feedback");
}

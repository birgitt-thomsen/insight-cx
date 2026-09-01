import { apiClient } from "./client";
import type { Feedback, FeedbackFilters, FeedbackPage } from "../types/feedback";

export function fetchFeedbackPage(filters: FeedbackFilters) {
  const params = new URLSearchParams();

  if (filters.page) params.set("page", String(filters.page));
  if (filters.search) params.set("search", filters.search);
  if (filters.survey_type) params.set("survey_type", filters.survey_type);
  if (filters.sentiment) params.set("sentiment", filters.sentiment);
  if (filters.priority) params.set("priority", filters.priority);

  const qs = params.toString();

  return apiClient.get<FeedbackPage>(`/feedback${qs ? `?${qs}` : ""}`);
}

export function fetchFeedbackDetail(id: number) {
  return apiClient.get<Feedback>(`/feedback/${id}`);
}

export function fetchTestSample() {
  return apiClient.get<{ items: Feedback[] }>("/feedback/test-sample");
}

export function reanalyzeFeedback(id: number) {
  return apiClient.post<Feedback>(`/feedback/${id}/reanalyze`);
}

export function toggleSample(id: number, selected: boolean) {
  return apiClient.post<{ sample_count: number }>(`/feedback/${id}/sample`, {
    selected,
  });
}

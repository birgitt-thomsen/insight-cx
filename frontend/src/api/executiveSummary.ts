import { apiClient } from "./client";
import type { ExecutiveInsight } from "../types/executiveSummary";

export interface ExecutiveSummaryLatestResponse {
  latest: ExecutiveInsight | null;
  previous: ExecutiveInsight | null;
  priority_counts: Record<string, number>;
}

export function fetchLatestExecutiveSummary() {
  return apiClient.get<ExecutiveSummaryLatestResponse>("/executive-summary/latest");
}

export interface GenerateExecutiveSummaryResult {
  summary: unknown;
  model: string;
  system_prompt_version: string;
  executive_prompt_version: string;
}

export function generateExecutiveSummary(model?: string) {
  return apiClient.post<GenerateExecutiveSummaryResult>(
    "/executive-summary/generate",
    { model },
  );
}

import { apiClient } from "./client";
import type { PromptTestRun } from "../types/aiEvaluation";

export interface AiEvaluationConfig {
  model?: string;
  temperature?: number;
  system_prompt_version?: string;
  feedback_prompt_version?: string;
}

export function runSingleFeedbackEvaluation(
  feedbackId: number,
  config: AiEvaluationConfig,
) {
  return apiClient.post<PromptTestRun>("/ai-evaluation/single", {
    feedback_id: feedbackId,
    ...config,
  });
}

export function runBenchmarkEvaluation(config: AiEvaluationConfig) {
  return apiClient.post<PromptTestRun>("/ai-evaluation/benchmark", config);
}

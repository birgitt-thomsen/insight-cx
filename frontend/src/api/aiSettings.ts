import { apiClient } from "./client";
import type { AISettings, PromptVersions } from "../types/aiSettings";

export interface AiSettingsResponse {
  settings: AISettings;
  prompt_versions: PromptVersions;
}

export function fetchAiSettings() {
  return apiClient.get<AiSettingsResponse>("/ai-settings");
}

export interface UpdateFeedbackSettingsPayload {
  model: string;
  temperature: number;
  system_prompt: string;
  feedback_prompt: string;
  description?: string;
}

export function updateFeedbackSettings(payload: UpdateFeedbackSettingsPayload) {
  return apiClient.post<AISettings>("/ai-settings/feedback", payload);
}

export interface UpdateExecutiveSettingsPayload {
  executive_model: string;
  executive_temperature: number;
  executive_prompt: string;
  description?: string;
}

export function updateExecutiveSettings(payload: UpdateExecutiveSettingsPayload) {
  return apiClient.post<AISettings>("/ai-settings/executive", payload);
}

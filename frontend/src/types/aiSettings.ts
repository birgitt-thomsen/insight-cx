export interface AISettings {
  feedback_model: string;
  feedback_temperature: number;
  system_prompt_version: string;
  feedback_prompt_version: string;
  executive_model: string;
  executive_temperature: number;
  executive_prompt_version: string;
  description: string | null;
  updated_at: string | null;
}

export interface PromptVersions {
  system: string[];
  feedback: string[];
  executive: string[];
}

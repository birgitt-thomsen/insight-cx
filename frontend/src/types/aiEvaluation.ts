import type { Analysis, ConfidenceLevel, Feedback, Priority, ReasonCode, Sentiment } from "./feedback";

/** The raw AI output for one test run, matching FEEDBACK_ANALYSIS_SCHEMA exactly. */
export interface AiOutputAnalysis {
  sentiment: Sentiment;
  emotions: string[];
  intent: string[];
  reason_codes: ReasonCode[];
  priority: Priority;
  confidence: {
    level: ConfidenceLevel;
    score: number;
    reason: string;
  };
  business_signal: string;
}

export interface PromptTestConfidenceStats {
  average_score: number;
  levels: Record<string, number>;
}

export interface PromptTestStatistics {
  sentiment: Record<string, number>;
  emotions: Record<string, number>;
  intent: Record<string, number>;
  priority: Record<string, number>;
  confidence: PromptTestConfidenceStats;
  reason_codes: [string, number][];
  primary_reason_codes: [string, number][];
  secondary_reason_codes: [string, number][];
  tertiary_reason_codes: [string, number][];
}

export interface PromptTestFailure {
  feedback_id: number;
  error: string | null;
}

export interface PromptTestItem {
  feedback: Feedback;
  current: Analysis | null;
  output: AiOutputAnalysis | null;
  error: string | null;
  changed_fields: string[];
}

export interface PromptTestRun {
  total: number;
  successful: number;
  failed: number;
  statistics: PromptTestStatistics;
  failures: PromptTestFailure[];
  results: PromptTestItem[];
}

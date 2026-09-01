export type Sentiment = "Positive" | "Neutral" | "Negative";
export type Priority = "High" | "Medium" | "Low";
export type ConfidenceLevel = "High" | "Medium" | "Low";

export interface ReasonCode {
  code: string;
  rank: number;
}

export interface Analysis {
  id: number;
  feedback_id: number;
  sentiment: Sentiment | null;
  emotions: string[] | null;
  intent: string[] | null;
  priority: Priority | null;
  confidence_score: number | null;
  confidence_level: ConfidenceLevel | null;
  reason_codes: ReasonCode[] | null;
  business_signal: string | null;
  analysis_json: Record<string, unknown> | null;
  model: string;
  system_prompt_version: string;
  feedback_prompt_version: string;
  analysis_version: number;
  analyzed_at: string | null;
}

export interface Feedback {
  id: number;
  customer_name: string;
  customer_id: string;
  order_number: string;
  comment: string;
  survey_type: string;
  score: number;
  nps_category: string | null;
  csat_category: string | null;
  source: string | null;
  feedback_date: string | null;
  uploaded_at: string | null;
  is_test_sample: boolean;
  analysis?: Analysis | null;
}

export interface FeedbackFilters {
  page?: number;
  search?: string;
  survey_type?: string;
  sentiment?: string;
  priority?: string;
}

export interface FeedbackPage {
  items: Feedback[];
  page: number;
  pages: number;
  per_page: number;
  total: number;
  has_next: boolean;
  has_prev: boolean;
  next_page: number | null;
  prev_page: number | null;
  sample_count: number;
  survey_types: string[];
}

export interface PeriodComparison {
  trend: "improving" | "declining" | "stable" | "unknown" | "up" | "down" | "new";
  summary: string;
}

export interface CustomerHealth {
  status: "Healthy" | "At Risk" | "Critical";
  color: "green" | "amber" | "red";
  headline: string;
  period_comparison: PeriodComparison;
}

export interface BusinessDriver {
  driver: string;
  count: number;
  summary: string;
  period_comparison: PeriodComparison;
}

export interface SentimentSummary {
  overall: string;
  positive_percentage: number;
  neutral_percentage: number;
  negative_percentage: number;
  insight: string;
}

export interface EmotionSummaryItem {
  emotion: string;
  percentage: number;
  business_meaning: string;
}

export interface LeadershipPriority {
  strategic_priority: string;
  business_objective: string;
  why_now: string;
  expected_business_value: string;
  executive_owner: string;
}

export interface RecommendedAction {
  action: string;
  details: string;
  priority: "High" | "Medium" | "Low";
  owner: string;
  timeframe: string;
  supports_priority: string[];
  success_measure: string;
}

export interface ConfidenceBlock {
  level: string;
  score: number;
  reason: string;
}

export interface AiRootCauseFinding {
  hypothesis: string;
  confidence: ConfidenceBlock;
  summary: string;
  evidence: string[];
  business_risk: string;
  recommended_validation: string;
  operational_validation: string;
}

export interface CustomerVerbatim {
  theme: string;
  comment: string;
}

export interface NpsInsight {
  interpretation: string;
  recommended_follow_up: string;
  promoter_percentage: number;
  passive_percentage: number;
  detractor_percentage: number;
}

export interface CsatInsight {
  interpretation: string;
  recommended_follow_up: string;
  satisfied_percentage: number;
  neutral_percentage: number;
  dissatisfied_percentage: number;
}

export interface KeyMetrics {
  feedback_count: number;
}

export interface EmergingBusinessSignal {
  signal_type: "Risk" | "Opportunity" | "Trend";
  business_signal: string;
  severity: "High" | "Medium" | "Low";
  likelihood: "Increasing" | "Stable" | "Emerging" | "Declining";
  description: string;
  leading_indicators: string[];
  recommended_monitoring: string;
  potential_impact: string;
}

export interface TopIntent {
  intent: string;
  percentage: number;
  business_meaning: string;
}

export interface IntentSummary {
  headline: string;
  insight: string;
  top_intents: TopIntent[];
}

export interface ExecutiveFocusItem {
  priority: string;
  why_it_matters: string;
}

export interface ExecutiveSummary {
  customer_health: CustomerHealth;
  executive_summary: string;
  business_impact: string;
  top_business_drivers: BusinessDriver[];
  sentiment_summary: SentimentSummary;
  emotion_summary: EmotionSummaryItem[];
  leadership_priorities: LeadershipPriority[];
  recommended_actions: RecommendedAction[];
  ai_root_cause_analysis: AiRootCauseFinding[];
  customer_verbatims: CustomerVerbatim[];
  nps_insight: NpsInsight;
  csat_insight: CsatInsight;
  confidence: ConfidenceBlock;
  key_metrics: KeyMetrics;
  emerging_business_signals: EmergingBusinessSignal[];
  intent_summary: IntentSummary;
  executive_focus: ExecutiveFocusItem[];
}

export interface ExecutiveInsight {
  id: number;
  summary: ExecutiveSummary;
  model: string;
  system_prompt_version: string;
  executive_prompt_version: string;
  generated_at: string | null;
}

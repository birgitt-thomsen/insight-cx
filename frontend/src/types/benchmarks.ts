export interface ModelComparisonEntry {
  benchmark_id: number;
  model: string;
  feedback_count: number;
  successful_tests: number;
  average_latency_ms: number;
  average_tokens: number;
  total_tokens: number;
  estimated_cost: number;
  average_cost_per_feedback: number;
  agreement_score: number;
  status: string;
}

export interface LatestBenchmark {
  completed_at: string | null;
  feedback_count: number;
}

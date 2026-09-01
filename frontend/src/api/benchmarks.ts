import { apiClient } from "./client";
import type { LatestBenchmark, ModelComparisonEntry } from "../types/benchmarks";

export interface BenchmarkComparisonResponse {
  comparison: ModelComparisonEntry[];
  latest_benchmark: LatestBenchmark | null;
}

export function fetchBenchmarkComparison() {
  return apiClient.get<BenchmarkComparisonResponse>("/benchmarks/comparison");
}

export function runBenchmarkComparison() {
  return apiClient.post<BenchmarkComparisonResponse>("/benchmarks/run");
}

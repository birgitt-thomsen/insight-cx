import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchBenchmarkComparison, runBenchmarkComparison } from "../../api/benchmarks";
import { Card, EmptyState, ErrorState, LoadingState } from "../../components";
import { formatCurrency, formatDateTime, formatNumber } from "../../lib/format";

const FIXED_MODELS = ["gpt-5-mini", "gpt-4.1-mini", "gpt-4o-mini"];

export function ModelComparisonTab() {
  const queryClient = useQueryClient();

  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ["benchmarks", "comparison"],
    queryFn: fetchBenchmarkComparison,
  });

  const runMutation = useMutation({
    mutationFn: runBenchmarkComparison,
    onSuccess: (result) => {
      queryClient.setQueryData(["benchmarks", "comparison"], result);
    },
  });

  const comparison = data?.comparison ?? [];

  return (
    <div className="space-y-6">
      <Card className="flex flex-wrap items-center justify-between gap-4 p-5">
        <div>
          <h3 className="text-sm font-semibold text-slate-900">Model Comparison</h3>
          <p className="mt-1 text-sm text-slate-500">
            Runs the same fixed feedback sample through {FIXED_MODELS.join(", ")} using system/feedback
            prompt v1, then compares speed, token usage, cost, and sentiment agreement.
          </p>
          {data?.latest_benchmark && (
            <p className="mt-2 text-xs text-slate-400">
              Latest benchmark: {formatDateTime(data.latest_benchmark.completed_at)} ·{" "}
              {data.latest_benchmark.feedback_count} feedback records · {comparison.length} models
            </p>
          )}
        </div>
        <button
          type="button"
          onClick={() => runMutation.mutate()}
          disabled={runMutation.isPending}
          className="whitespace-nowrap rounded-md bg-teal-800 px-4 py-2 text-sm font-medium text-white hover:bg-teal-900 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {runMutation.isPending ? "Running comparison…" : "Run Model Comparison"}
        </button>
      </Card>

      {isLoading && <LoadingState label="Loading the latest comparison…" />}

      {isError && (
        <ErrorState
          description={
            error instanceof Error ? error.message : "Could not load the benchmark comparison."
          }
          onRetry={() => refetch()}
        />
      )}

      {runMutation.isError && (
        <ErrorState
          title="Comparison run failed"
          description={
            runMutation.error instanceof Error ? runMutation.error.message : "The comparison run failed."
          }
        />
      )}

      {!isLoading && !isError && comparison.length === 0 && (
        <EmptyState
          title="No comparison run yet"
          description="Run the model comparison to see latency, token usage, cost, and sentiment agreement side by side."
        />
      )}

      {comparison.length > 0 && (
        <>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {comparison.map((model) => (
              <Card key={model.model} className="p-5">
                <h4 className="text-sm font-semibold text-slate-900">{model.model}</h4>
                <dl className="mt-3 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <dt className="text-slate-500">Avg. Latency</dt>
                    <dd className="font-medium text-slate-800">
                      {(model.average_latency_ms / 1000).toFixed(2)}s
                    </dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-slate-500">Avg. Tokens</dt>
                    <dd className="font-medium text-slate-800">{formatNumber(model.average_tokens)}</dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-slate-500">Total Cost</dt>
                    <dd className="font-medium text-slate-800">
                      {formatCurrency(model.estimated_cost, 5)}
                    </dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-slate-500">Cost / Feedback</dt>
                    <dd className="font-medium text-slate-800">
                      {formatCurrency(model.average_cost_per_feedback, 6)}
                    </dd>
                  </div>
                  <div className="flex justify-between">
                    <dt className="text-slate-500">Sentiment Agreement</dt>
                    <dd className="font-medium text-slate-800">{model.agreement_score}%</dd>
                  </div>
                </dl>
              </Card>
            ))}
          </div>

          <Card className="overflow-x-auto p-5">
            <h3 className="text-sm font-semibold text-slate-900">Performance Comparison</h3>
            <table className="mt-3 w-full min-w-[640px] text-left text-sm">
              <thead>
                <tr className="border-b border-slate-200 text-xs font-medium uppercase tracking-wide text-slate-500">
                  <th scope="col" className="py-2 pr-4">
                    Metric
                  </th>
                  {comparison.map((model) => (
                    <th key={model.model} scope="col" className="py-2 pr-4">
                      {model.model}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                <tr>
                  <td className="py-2 pr-4 text-slate-500">Feedback Tested</td>
                  {comparison.map((model) => (
                    <td key={model.model} className="py-2 pr-4 text-slate-700">
                      {model.feedback_count}
                    </td>
                  ))}
                </tr>
                <tr>
                  <td className="py-2 pr-4 text-slate-500">Avg. Latency</td>
                  {comparison.map((model) => (
                    <td key={model.model} className="py-2 pr-4 text-slate-700">
                      {(model.average_latency_ms / 1000).toFixed(2)}s
                    </td>
                  ))}
                </tr>
                <tr>
                  <td className="py-2 pr-4 text-slate-500">Avg. Tokens</td>
                  {comparison.map((model) => (
                    <td key={model.model} className="py-2 pr-4 text-slate-700">
                      {formatNumber(model.average_tokens)}
                    </td>
                  ))}
                </tr>
                <tr>
                  <td className="py-2 pr-4 text-slate-500">Total Tokens</td>
                  {comparison.map((model) => (
                    <td key={model.model} className="py-2 pr-4 text-slate-700">
                      {formatNumber(model.total_tokens)}
                    </td>
                  ))}
                </tr>
                <tr>
                  <td className="py-2 pr-4 text-slate-500">Total Cost</td>
                  {comparison.map((model) => (
                    <td key={model.model} className="py-2 pr-4 text-slate-700">
                      {formatCurrency(model.estimated_cost, 5)}
                    </td>
                  ))}
                </tr>
                <tr>
                  <td className="py-2 pr-4 text-slate-500">Cost / Feedback</td>
                  {comparison.map((model) => (
                    <td key={model.model} className="py-2 pr-4 text-slate-700">
                      {formatCurrency(model.average_cost_per_feedback, 6)}
                    </td>
                  ))}
                </tr>
                <tr>
                  <td className="py-2 pr-4 text-slate-500">Sentiment Agreement</td>
                  {comparison.map((model) => (
                    <td key={model.model} className="py-2 pr-4 text-slate-700">
                      {model.agreement_score}%
                    </td>
                  ))}
                </tr>
                <tr>
                  <td className="py-2 pr-4 text-slate-500">Successful Tests</td>
                  {comparison.map((model) => (
                    <td key={model.model} className="py-2 pr-4 text-slate-700">
                      {model.successful_tests} / {model.feedback_count}
                    </td>
                  ))}
                </tr>
              </tbody>
            </table>
          </Card>
        </>
      )}
    </div>
  );
}

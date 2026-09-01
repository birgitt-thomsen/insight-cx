import { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery } from "@tanstack/react-query";
import { runBenchmarkEvaluation } from "../../api/aiEvaluation";
import { fetchTestSample } from "../../api/feedback";
import type { AiSettingsResponse } from "../../api/aiSettings";
import { Badge, Card, EmptyState, ErrorState, LoadingState, MetricCard } from "../../components";
import { AnalysisComparisonGrid } from "./AnalysisComparisonGrid";
import { DistributionCard } from "./DistributionCard";
import { EvaluationConfigCard, type EvaluationConfig } from "./EvaluationConfigCard";

const DEFAULT_CONFIG: EvaluationConfig = {
  model: "gpt-5-mini",
  temperature: 0.2,
  systemPromptVersion: "v1",
  feedbackPromptVersion: "v1",
};

export function BenchmarkLabTab({ aiSettings }: { aiSettings: AiSettingsResponse | undefined }) {
  const [config, setConfig] = useState<EvaluationConfig>(DEFAULT_CONFIG);
  const initializedRef = useRef(false);

  useEffect(() => {
    if (!initializedRef.current && aiSettings) {
      setConfig({
        model: aiSettings.settings.feedback_model,
        temperature: aiSettings.settings.feedback_temperature,
        systemPromptVersion: aiSettings.settings.system_prompt_version,
        feedbackPromptVersion: aiSettings.settings.feedback_prompt_version,
      });
      initializedRef.current = true;
    }
  }, [aiSettings]);

  const sampleQuery = useQuery({
    queryKey: ["feedback", "test-sample"],
    queryFn: fetchTestSample,
  });

  const runMutation = useMutation({
    mutationFn: () =>
      runBenchmarkEvaluation({
        model: config.model,
        temperature: config.model.startsWith("gpt-5") ? undefined : config.temperature,
        system_prompt_version: config.systemPromptVersion,
        feedback_prompt_version: config.feedbackPromptVersion,
      }),
  });

  const sampleRecords = sampleQuery.data?.items ?? [];
  const result = runMutation.data;

  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-2">
        <EvaluationConfigCard
          config={config}
          onChange={setConfig}
          promptVersions={aiSettings?.prompt_versions}
          description="Define the model and prompt combination to evaluate against the benchmark sample."
        />

        <Card className="p-5">
          <div className="flex items-start justify-between gap-3">
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-semibold text-slate-900">Benchmark Dataset</h3>
                {!sampleQuery.isLoading && <Badge>{sampleRecords.length} records</Badge>}
              </div>
              <p className="mt-1 text-sm text-slate-500">
                The feedback records currently flagged as the benchmark sample in Feedback Explorer.
              </p>
            </div>
            <Link
              to="/feedback-explorer"
              className="whitespace-nowrap text-sm font-medium text-teal-800 hover:text-teal-900"
            >
              Manage sample →
            </Link>
          </div>

          {sampleQuery.isLoading && <LoadingState label="Loading sample…" />}

          {!sampleQuery.isLoading && sampleRecords.length === 0 && (
            <EmptyState
              title="No records in the benchmark sample"
              description="Select feedback records using the Sample column in Feedback Explorer before running a benchmark."
            />
          )}

          {sampleRecords.length > 0 && (
            <ul className="mt-3 max-h-64 space-y-2 overflow-y-auto">
              {sampleRecords.map((record) => (
                <li key={record.id} className="rounded-lg border border-slate-200 p-3 text-sm">
                  <p className="font-medium text-slate-800">
                    {record.customer_name} · {record.survey_type} {record.score}
                  </p>
                  <p className="mt-0.5 truncate text-slate-500">{record.comment}</p>
                </li>
              ))}
            </ul>
          )}

          <button
            type="button"
            onClick={() => runMutation.mutate()}
            disabled={sampleRecords.length === 0 || runMutation.isPending}
            className="mt-4 rounded-md bg-teal-800 px-4 py-2 text-sm font-medium text-white hover:bg-teal-900 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {runMutation.isPending ? "Running evaluation…" : "Run Evaluation"}
          </button>
        </Card>
      </div>

      {runMutation.isPending && <LoadingState label="Running benchmark evaluation…" />}

      {runMutation.isError && (
        <ErrorState
          title="Evaluation failed"
          description={
            runMutation.error instanceof Error ? runMutation.error.message : "The benchmark run failed."
          }
          onRetry={() => runMutation.mutate()}
        />
      )}

      {!runMutation.isPending && !runMutation.isError && !result && (
        <EmptyState
          title="No evaluation run yet"
          description="Choose the model and prompt configuration to evaluate, then run it against the benchmark sample to compare against the analyses currently stored in InsightCX."
        />
      )}

      {result && (
        <div className="space-y-6">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <MetricCard label="Processed" value={String(result.total)} />
            <MetricCard label="Successful" value={String(result.successful)} />
            <MetricCard label="Failed" value={String(result.failed)} />
            <MetricCard label="Avg Confidence" value={`${result.statistics.confidence.average_score}%`} />
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <DistributionCard
              title="Sentiment"
              columnLabel="Sentiment"
              entries={Object.entries(result.statistics.sentiment)}
            />
            <DistributionCard
              title="Priority"
              columnLabel="Priority"
              entries={Object.entries(result.statistics.priority)}
            />
            <DistributionCard
              title="Customer Intent"
              columnLabel="Intent"
              entries={Object.entries(result.statistics.intent)}
            />
            <DistributionCard
              title="Emotions"
              columnLabel="Emotion"
              entries={Object.entries(result.statistics.emotions)}
            />
            <DistributionCard
              title="Confidence Levels"
              columnLabel="Level"
              entries={Object.entries(result.statistics.confidence.levels)}
            />
            <DistributionCard
              title="Top Reason Codes"
              columnLabel="Reason Code"
              entries={result.statistics.reason_codes}
            />
          </div>

          <div>
            <h3 className="text-sm font-semibold text-slate-900">Individual Results</h3>
            <div className="mt-3 space-y-2">
              {result.results.map((item) => (
                <details
                  key={item.feedback.id}
                  className="rounded-lg border border-slate-200 bg-white p-4"
                >
                  <summary className="cursor-pointer text-sm font-medium text-slate-700">
                    {item.feedback.customer_name} · Feedback #{item.feedback.id}
                    {item.error && <span className="ml-2 text-rose-600">(failed)</span>}
                  </summary>
                  <div className="mt-3">
                    <p className="text-sm text-slate-600">{item.feedback.comment}</p>
                    {item.error ? (
                      <div className="mt-3">
                        <ErrorState title="This item failed" description={item.error} />
                      </div>
                    ) : item.output ? (
                      <div className="mt-3">
                        <p className="mb-2 text-xs font-medium text-slate-500">
                          {item.changed_fields.length} field(s) changed from the current analysis
                        </p>
                        <AnalysisComparisonGrid
                          current={item.current}
                          output={item.output}
                          changedFields={item.changed_fields}
                        />
                      </div>
                    ) : null}
                  </div>
                </details>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

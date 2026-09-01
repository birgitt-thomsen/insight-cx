import { useEffect, useRef, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { runSingleFeedbackEvaluation } from "../../api/aiEvaluation";
import { fetchFeedbackDetail, fetchFeedbackPage } from "../../api/feedback";
import type { AiSettingsResponse } from "../../api/aiSettings";
import { Card, EmptyState, ErrorState, LoadingState } from "../../components";
import type { Feedback } from "../../types/feedback";
import { AnalysisComparisonGrid } from "./AnalysisComparisonGrid";
import { EvaluationConfigCard, type EvaluationConfig } from "./EvaluationConfigCard";

const DEFAULT_CONFIG: EvaluationConfig = {
  model: "gpt-5-mini",
  temperature: 0.2,
  systemPromptVersion: "v1",
  feedbackPromptVersion: "v1",
};

export function SingleFeedbackTab({
  aiSettings,
  initialFeedbackId,
}: {
  aiSettings: AiSettingsResponse | undefined;
  initialFeedbackId: number | null;
}) {
  const [config, setConfig] = useState<EvaluationConfig>(DEFAULT_CONFIG);
  const initializedRef = useRef(false);

  // Seed the test configuration from the current production settings the
  // first time they load, without ever overwriting the user's own edits.
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

  const [selectedFeedback, setSelectedFeedback] = useState<Feedback | null>(null);
  const [search, setSearch] = useState("");
  const [showResults, setShowResults] = useState(false);

  const initialFeedbackQuery = useQuery({
    queryKey: ["feedback", "detail", initialFeedbackId],
    queryFn: () => fetchFeedbackDetail(initialFeedbackId!),
    enabled: initialFeedbackId !== null,
  });

  useEffect(() => {
    if (initialFeedbackQuery.data) {
      setSelectedFeedback(initialFeedbackQuery.data);
    }
  }, [initialFeedbackQuery.data]);

  const searchQuery = useQuery({
    queryKey: ["feedback", "picker-search", search],
    queryFn: () => fetchFeedbackPage({ search, page: 1 }),
    enabled: search.trim().length >= 2,
  });

  const runMutation = useMutation({
    mutationFn: () =>
      runSingleFeedbackEvaluation(selectedFeedback!.id, {
        model: config.model,
        temperature: config.model.startsWith("gpt-5") ? undefined : config.temperature,
        system_prompt_version: config.systemPromptVersion,
        feedback_prompt_version: config.feedbackPromptVersion,
      }),
  });

  const result = runMutation.data;
  const item = result?.results[0];
  const failure = result?.failures[0];

  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="space-y-6">
        <EvaluationConfigCard
          config={config}
          onChange={setConfig}
          promptVersions={aiSettings?.prompt_versions}
          description="These settings are applied to this run only and never change the production configuration."
        />

        <Card className="p-5">
          <h3 className="text-sm font-semibold text-slate-900">Customer Feedback</h3>
          <p className="mt-1 text-sm text-slate-500">Search for a feedback record to test.</p>

          <div className="relative mt-3">
            <input
              type="text"
              value={search}
              onChange={(event) => {
                setSearch(event.target.value);
                setShowResults(true);
              }}
              onFocus={() => setShowResults(true)}
              placeholder="Search by customer, order ID or comment…"
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
            />

            {showResults && search.trim().length >= 2 && (
              <div className="absolute z-10 mt-1 w-full rounded-md border border-slate-200 bg-white shadow-lg">
                {searchQuery.isLoading && (
                  <p className="px-3 py-2 text-sm text-slate-500">Searching…</p>
                )}
                {searchQuery.data && searchQuery.data.items.length === 0 && (
                  <p className="px-3 py-2 text-sm text-slate-500">No matching feedback found.</p>
                )}
                {searchQuery.data?.items.slice(0, 6).map((record) => (
                  <button
                    key={record.id}
                    type="button"
                    onClick={() => {
                      setSelectedFeedback(record);
                      setSearch("");
                      setShowResults(false);
                    }}
                    className="block w-full border-b border-slate-100 px-3 py-2 text-left text-sm last:border-0 hover:bg-slate-50"
                  >
                    <span className="font-medium text-slate-800">{record.customer_name}</span>{" "}
                    <span className="text-slate-400">
                      · {record.survey_type} {record.score}
                    </span>
                    <p className="truncate text-xs text-slate-500">{record.comment}</p>
                  </button>
                ))}
              </div>
            )}
          </div>

          {selectedFeedback ? (
            <div className="mt-4 rounded-lg border border-slate-200 bg-slate-50 p-3">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                {selectedFeedback.customer_name} · {selectedFeedback.survey_type}{" "}
                {selectedFeedback.score}
              </p>
              <p className="mt-1 text-sm text-slate-700">{selectedFeedback.comment}</p>
            </div>
          ) : (
            <p className="mt-4 text-sm text-slate-400">No feedback record selected yet.</p>
          )}

          <button
            type="button"
            onClick={() => runMutation.mutate()}
            disabled={!selectedFeedback || runMutation.isPending}
            className="mt-4 rounded-md bg-teal-800 px-4 py-2 text-sm font-medium text-white hover:bg-teal-900 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {runMutation.isPending ? "Running analysis…" : "Run Analysis"}
          </button>
        </Card>
      </div>

      <Card className="p-5">
        <h3 className="text-sm font-semibold text-slate-900">AI Analysis Result</h3>
        <p className="mt-1 text-sm text-slate-500">
          Input → AI analysis → structured result, using the same fields as production analysis.
        </p>

        <div className="mt-4">
          {runMutation.isPending && <LoadingState label="Running analysis…" />}

          {runMutation.isError && (
            <ErrorState
              description={
                runMutation.error instanceof Error ? runMutation.error.message : "The test run failed."
              }
              onRetry={() => runMutation.mutate()}
            />
          )}

          {!runMutation.isPending && !runMutation.isError && !result && (
            <EmptyState
              title="No result yet"
              description="Configure the model and prompts, choose a feedback record, and run the analysis."
            />
          )}

          {result && failure && (
            <ErrorState title="Analysis failed" description={failure.error ?? undefined} />
          )}

          {result && item?.output && (
            <div>
              <p className="mb-3 text-sm font-medium text-slate-600">
                {item.changed_fields.length} field(s) changed from the current analysis
              </p>
              <AnalysisComparisonGrid
                current={item.current}
                output={item.output}
                changedFields={item.changed_fields}
              />
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}

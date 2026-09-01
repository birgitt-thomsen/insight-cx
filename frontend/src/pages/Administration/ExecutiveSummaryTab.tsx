import { useState } from "react";
import { Link } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchLatestExecutiveSummary, generateExecutiveSummary } from "../../api/executiveSummary";
import type { AiSettingsResponse } from "../../api/aiSettings";
import { Card, ErrorState, LoadingState } from "../../components";
import { formatDateTime } from "../../lib/format";
import { Field } from "./Field";

const MODEL_OPTIONS = [
  { value: "gpt-5-mini", label: "GPT-5 mini" },
  { value: "gpt-4.1-mini", label: "GPT-4.1 mini" },
  { value: "gpt-4o-mini", label: "GPT-4o mini" },
];

function InfoTile({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-slate-200 p-4">
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">{label}</p>
      <p className="mt-1 text-sm font-medium text-slate-800">{value}</p>
    </div>
  );
}

export function ExecutiveSummaryTab({ aiSettings }: { aiSettings: AiSettingsResponse | undefined }) {
  const queryClient = useQueryClient();
  const [model, setModel] = useState("");

  const latestQuery = useQuery({
    queryKey: ["executive-summary", "latest"],
    queryFn: fetchLatestExecutiveSummary,
  });

  const generateMutation = useMutation({
    mutationFn: () => generateExecutiveSummary(model || undefined),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["executive-summary"] });
    },
  });

  const latest = latestQuery.data?.latest;
  const selectedModel = model || aiSettings?.settings.executive_model || "gpt-5-mini";

  return (
    <div className="space-y-6">
      <Card className="p-5">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h3 className="text-sm font-semibold text-slate-900">Executive Summary Generation</h3>
            <p className="mt-1 text-sm text-slate-500">
              Runs the executive prompt across the full analyzed dataset and republishes the
              Executive Brief.
            </p>
          </div>
          <div className="flex items-end gap-3">
            <Field label="Model">
              <select
                value={selectedModel}
                onChange={(event) => setModel(event.target.value)}
                className="rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-700 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              >
                {MODEL_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </Field>
            <button
              type="button"
              onClick={() => generateMutation.mutate()}
              disabled={generateMutation.isPending}
              className="whitespace-nowrap rounded-md bg-teal-800 px-4 py-2 text-sm font-medium text-white hover:bg-teal-900 disabled:opacity-50"
            >
              {generateMutation.isPending ? "Generating…" : "Generate Summary"}
            </button>
          </div>
        </div>

        {generateMutation.isError && (
          <div className="mt-4">
            <ErrorState
              title="Generation failed"
              description={
                generateMutation.error instanceof Error
                  ? generateMutation.error.message
                  : "Could not generate the executive summary."
              }
            />
          </div>
        )}

        <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <InfoTile
            label="Status"
            value={generateMutation.isPending ? "Generating…" : latest ? "Complete" : "Not generated yet"}
          />
          <InfoTile label="Latest Generation" value={formatDateTime(latest?.generated_at)} />
          <InfoTile label="Model Used" value={latest?.model ?? "—"} />
          <InfoTile label="Executive Prompt Version" value={latest?.executive_prompt_version ?? "—"} />
          <InfoTile
            label="Records Considered"
            value={latest ? latest.summary.key_metrics.feedback_count.toLocaleString() : "—"}
          />
          <InfoTile label="Customer Health" value={latest?.summary.customer_health.status ?? "—"} />
        </div>
      </Card>

      {latestQuery.isLoading && <LoadingState label="Loading the latest summary…" />}

      {latest && (
        <Card className="p-5">
          <h3 className="text-sm font-semibold text-slate-900">Generated Summary Preview</h3>
          <p className="mt-1 text-sm text-slate-500">How the current generation reads for leadership.</p>

          <div className="mt-4 rounded-lg border border-indigo-100 bg-indigo-50 p-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">Headline</p>
            <p className="mt-1 text-sm font-medium text-indigo-900">
              {latest.summary.customer_health.headline}
            </p>
          </div>

          <p className="mt-4 text-sm text-slate-700">{latest.summary.executive_summary}</p>

          <div className="mt-4 flex flex-wrap items-center gap-3">
            <Link
              to="/executive-brief"
              className="rounded-md bg-teal-800 px-3 py-2 text-sm font-medium text-white hover:bg-teal-900"
            >
              View full Executive Brief →
            </Link>

            <details className="text-sm text-slate-500">
              <summary className="cursor-pointer font-medium text-slate-600">Raw JSON response</summary>
              <pre className="mt-2 max-h-96 overflow-auto rounded-lg bg-slate-900 p-3 text-xs text-slate-100">
                {JSON.stringify(latest.summary, null, 2)}
              </pre>
            </details>
          </div>
        </Card>
      )}
    </div>
  );
}

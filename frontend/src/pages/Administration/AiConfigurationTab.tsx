import { useEffect, useRef, useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { updateExecutiveSettings, updateFeedbackSettings } from "../../api/aiSettings";
import type { AiSettingsResponse } from "../../api/aiSettings";
import { Card } from "../../components";
import { Field } from "./Field";

const MODEL_OPTIONS = [
  { value: "gpt-5-mini", label: "GPT-5 mini" },
  { value: "gpt-4o-mini", label: "GPT-4o mini" },
  { value: "gpt-4.1-mini", label: "GPT-4.1 mini" },
];

const fieldClass =
  "rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-700 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 disabled:bg-slate-100 disabled:text-slate-400";

export function AiConfigurationTab({ aiSettings }: { aiSettings: AiSettingsResponse | undefined }) {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <FeedbackAnalysisCard aiSettings={aiSettings} />
      <ExecutiveAnalysisCard aiSettings={aiSettings} />
    </div>
  );
}

function SaveStatus({
  isPending,
  isSuccess,
  isError,
  errorMessage,
}: {
  isPending: boolean;
  isSuccess: boolean;
  isError: boolean;
  errorMessage?: string;
}) {
  if (isPending) return null;
  if (isSuccess) return <span className="text-sm font-medium text-emerald-600">✓ Saved</span>;
  if (isError) return <span className="text-sm font-medium text-rose-600">{errorMessage}</span>;
  return null;
}

function FeedbackAnalysisCard({ aiSettings }: { aiSettings: AiSettingsResponse | undefined }) {
  const queryClient = useQueryClient();
  const [model, setModel] = useState("gpt-5-mini");
  const [temperature, setTemperature] = useState(0.2);
  const [systemPrompt, setSystemPrompt] = useState("v1");
  const [feedbackPrompt, setFeedbackPrompt] = useState("v1");
  const [description, setDescription] = useState("");
  const initializedRef = useRef(false);

  useEffect(() => {
    if (!initializedRef.current && aiSettings) {
      setModel(aiSettings.settings.feedback_model);
      setTemperature(aiSettings.settings.feedback_temperature);
      setSystemPrompt(aiSettings.settings.system_prompt_version);
      setFeedbackPrompt(aiSettings.settings.feedback_prompt_version);
      setDescription(aiSettings.settings.description ?? "");
      initializedRef.current = true;
    }
  }, [aiSettings]);

  const mutation = useMutation({
    mutationFn: () =>
      updateFeedbackSettings({
        model,
        temperature,
        system_prompt: systemPrompt,
        feedback_prompt: feedbackPrompt,
        description,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ai-settings"] });
    },
  });

  const supportsTemperature = !model.startsWith("gpt-5");

  return (
    <Card className="p-5">
      <h3 className="text-sm font-semibold text-slate-900">Feedback Analysis</h3>
      <p className="mt-1 text-sm text-slate-500">
        Applied to every individual feedback record on import and re-analysis.
      </p>

      <form
        className="mt-4 space-y-4"
        onChangeCapture={() => {
          if (mutation.isSuccess || mutation.isError) mutation.reset();
        }}
        onSubmit={(event) => {
          event.preventDefault();
          mutation.mutate();
        }}
      >
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Model">
            <select value={model} onChange={(event) => setModel(event.target.value)} className={fieldClass}>
              {MODEL_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </Field>

          <Field label="Temperature" hint={!supportsTemperature ? "Ignored by GPT-5 models." : undefined}>
            <input
              type="number"
              min={0}
              max={2}
              step={0.1}
              value={temperature}
              disabled={!supportsTemperature}
              onChange={(event) => setTemperature(Number(event.target.value))}
              className={fieldClass}
            />
          </Field>

          <Field label="System Prompt">
            <select
              value={systemPrompt}
              onChange={(event) => setSystemPrompt(event.target.value)}
              className={fieldClass}
            >
              {(aiSettings?.prompt_versions.system ?? [systemPrompt]).map((version) => (
                <option key={version} value={version}>
                  {version}
                </option>
              ))}
            </select>
          </Field>

          <Field label="Feedback Prompt">
            <select
              value={feedbackPrompt}
              onChange={(event) => setFeedbackPrompt(event.target.value)}
              className={fieldClass}
            >
              {(aiSettings?.prompt_versions.feedback ?? [feedbackPrompt]).map((version) => (
                <option key={version} value={version}>
                  {version}
                </option>
              ))}
            </select>
          </Field>
        </div>

        <Field label="Release Notes">
          <textarea
            rows={3}
            value={description}
            onChange={(event) => setDescription(event.target.value)}
            placeholder="Describe what changed in this AI configuration."
            className={fieldClass}
          />
        </Field>

        <div className="flex items-center gap-3">
          <button
            type="submit"
            disabled={mutation.isPending}
            className="rounded-md bg-teal-800 px-4 py-2 text-sm font-medium text-white hover:bg-teal-900 disabled:opacity-50"
          >
            {mutation.isPending ? "Saving…" : "Save Feedback Settings"}
          </button>
          <SaveStatus
            isPending={mutation.isPending}
            isSuccess={mutation.isSuccess}
            isError={mutation.isError}
            errorMessage={mutation.error instanceof Error ? mutation.error.message : "Save failed."}
          />
        </div>
      </form>
    </Card>
  );
}

function ExecutiveAnalysisCard({ aiSettings }: { aiSettings: AiSettingsResponse | undefined }) {
  const queryClient = useQueryClient();
  const [model, setModel] = useState("gpt-5-mini");
  const [temperature, setTemperature] = useState(0.2);
  const [executivePrompt, setExecutivePrompt] = useState("v1");
  const initializedRef = useRef(false);

  useEffect(() => {
    if (!initializedRef.current && aiSettings) {
      setModel(aiSettings.settings.executive_model);
      setTemperature(aiSettings.settings.executive_temperature);
      setExecutivePrompt(aiSettings.settings.executive_prompt_version);
      initializedRef.current = true;
    }
  }, [aiSettings]);

  const mutation = useMutation({
    mutationFn: () =>
      updateExecutiveSettings({
        executive_model: model,
        executive_temperature: temperature,
        executive_prompt: executivePrompt,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["ai-settings"] });
    },
  });

  const supportsTemperature = !model.startsWith("gpt-5");

  return (
    <Card className="p-5">
      <h3 className="text-sm font-semibold text-slate-900">Executive Analysis</h3>
      <p className="mt-1 text-sm text-slate-500">
        Applied when generating the Executive Brief from the full analyzed dataset.
      </p>

      <form
        className="mt-4 space-y-4"
        onChangeCapture={() => {
          if (mutation.isSuccess || mutation.isError) mutation.reset();
        }}
        onSubmit={(event) => {
          event.preventDefault();
          mutation.mutate();
        }}
      >
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Model">
            <select value={model} onChange={(event) => setModel(event.target.value)} className={fieldClass}>
              {MODEL_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </Field>

          <Field label="Temperature" hint={!supportsTemperature ? "Ignored by GPT-5 models." : undefined}>
            <input
              type="number"
              min={0}
              max={2}
              step={0.1}
              value={temperature}
              disabled={!supportsTemperature}
              onChange={(event) => setTemperature(Number(event.target.value))}
              className={fieldClass}
            />
          </Field>

          <Field label="Executive Prompt">
            <select
              value={executivePrompt}
              onChange={(event) => setExecutivePrompt(event.target.value)}
              className={fieldClass}
            >
              {(aiSettings?.prompt_versions.executive ?? [executivePrompt]).map((version) => (
                <option key={version} value={version}>
                  {version}
                </option>
              ))}
            </select>
          </Field>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="submit"
            disabled={mutation.isPending}
            className="rounded-md bg-teal-800 px-4 py-2 text-sm font-medium text-white hover:bg-teal-900 disabled:opacity-50"
          >
            {mutation.isPending ? "Saving…" : "Save Executive Settings"}
          </button>
          <SaveStatus
            isPending={mutation.isPending}
            isSuccess={mutation.isSuccess}
            isError={mutation.isError}
            errorMessage={mutation.error instanceof Error ? mutation.error.message : "Save failed."}
          />
        </div>
      </form>
    </Card>
  );
}

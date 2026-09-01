import { Card } from "../../components";
import type { PromptVersions } from "../../types/aiSettings";

export interface EvaluationConfig {
  model: string;
  temperature: number;
  systemPromptVersion: string;
  feedbackPromptVersion: string;
}

const MODEL_OPTIONS = [
  { value: "gpt-5-mini", label: "GPT-5 mini" },
  { value: "gpt-4o-mini", label: "GPT-4o mini" },
  { value: "gpt-4.1-mini", label: "GPT-4.1 mini" },
];

const fieldClass =
  "rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-700 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 disabled:bg-slate-100 disabled:text-slate-400";

export function EvaluationConfigCard({
  config,
  onChange,
  promptVersions,
  title = "Test Configuration",
  description,
}: {
  config: EvaluationConfig;
  onChange: (config: EvaluationConfig) => void;
  promptVersions: PromptVersions | undefined;
  title?: string;
  description?: string;
}) {
  const supportsTemperature = !config.model.startsWith("gpt-5");

  return (
    <Card className="p-5">
      <h3 className="text-sm font-semibold text-slate-900">{title}</h3>
      {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}

      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-slate-500" htmlFor="eval-model">
            Model
          </label>
          <select
            id="eval-model"
            value={config.model}
            onChange={(event) => onChange({ ...config, model: event.target.value })}
            className={fieldClass}
          >
            {MODEL_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-slate-500" htmlFor="eval-temperature">
            Temperature
          </label>
          <input
            id="eval-temperature"
            type="number"
            min={0}
            max={2}
            step={0.1}
            value={config.temperature}
            disabled={!supportsTemperature}
            onChange={(event) => onChange({ ...config, temperature: Number(event.target.value) })}
            className={fieldClass}
          />
          {!supportsTemperature && (
            <p className="text-xs text-slate-400">Temperature is ignored by GPT-5 models.</p>
          )}
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-slate-500" htmlFor="eval-system-prompt">
            System Prompt
          </label>
          <select
            id="eval-system-prompt"
            value={config.systemPromptVersion}
            onChange={(event) => onChange({ ...config, systemPromptVersion: event.target.value })}
            className={fieldClass}
          >
            {(promptVersions?.system ?? [config.systemPromptVersion]).map((version) => (
              <option key={version} value={version}>
                {version}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-xs font-medium text-slate-500" htmlFor="eval-feedback-prompt">
            Feedback Prompt
          </label>
          <select
            id="eval-feedback-prompt"
            value={config.feedbackPromptVersion}
            onChange={(event) => onChange({ ...config, feedbackPromptVersion: event.target.value })}
            className={fieldClass}
          >
            {(promptVersions?.feedback ?? [config.feedbackPromptVersion]).map((version) => (
              <option key={version} value={version}>
                {version}
              </option>
            ))}
          </select>
        </div>
      </div>
    </Card>
  );
}

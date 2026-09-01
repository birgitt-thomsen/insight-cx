import { useEffect, useState } from "react";
import type { FeedbackFilters } from "../../types/feedback";

const inputClass =
  "rounded-md border border-slate-300 px-3 py-2 text-sm text-slate-700 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500";

export function FeedbackFiltersBar({
  filters,
  surveyTypes,
  onApply,
  onClear,
}: {
  filters: Omit<FeedbackFilters, "page">;
  surveyTypes: string[];
  onApply: (filters: Omit<FeedbackFilters, "page">) => void;
  onClear: () => void;
}) {
  const [draft, setDraft] = useState(filters);

  // Re-sync the draft whenever the committed filters change from outside
  // this form (e.g. a link from Executive Brief prefilling the search box,
  // or the browser back/forward buttons).
  useEffect(() => {
    setDraft(filters);
  }, [filters.search, filters.survey_type, filters.sentiment, filters.priority]);

  return (
    <form
      className="flex flex-wrap items-end gap-3"
      onSubmit={(event) => {
        event.preventDefault();
        onApply(draft);
      }}
    >
      <div className="flex min-w-[220px] flex-1 flex-col gap-1">
        <label htmlFor="feedback-search" className="text-xs font-medium text-slate-500">
          Search
        </label>
        <input
          id="feedback-search"
          type="text"
          value={draft.search ?? ""}
          onChange={(event) => setDraft((prev) => ({ ...prev, search: event.target.value }))}
          placeholder="Customer, order ID or feedback text…"
          className={inputClass}
        />
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="feedback-survey-type" className="text-xs font-medium text-slate-500">
          Survey
        </label>
        <select
          id="feedback-survey-type"
          value={draft.survey_type ?? ""}
          onChange={(event) => setDraft((prev) => ({ ...prev, survey_type: event.target.value }))}
          className={inputClass}
        >
          <option value="">All surveys</option>
          {surveyTypes.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="feedback-sentiment" className="text-xs font-medium text-slate-500">
          Sentiment
        </label>
        <select
          id="feedback-sentiment"
          value={draft.sentiment ?? ""}
          onChange={(event) => setDraft((prev) => ({ ...prev, sentiment: event.target.value }))}
          className={inputClass}
        >
          <option value="">All sentiment</option>
          <option value="Positive">Positive</option>
          <option value="Neutral">Neutral</option>
          <option value="Negative">Negative</option>
        </select>
      </div>

      <div className="flex flex-col gap-1">
        <label htmlFor="feedback-priority" className="text-xs font-medium text-slate-500">
          Priority
        </label>
        <select
          id="feedback-priority"
          value={draft.priority ?? ""}
          onChange={(event) => setDraft((prev) => ({ ...prev, priority: event.target.value }))}
          className={inputClass}
        >
          <option value="">All priorities</option>
          <option value="High">High</option>
          <option value="Medium">Medium</option>
          <option value="Low">Low</option>
        </select>
      </div>

      <div className="flex gap-2">
        <button
          type="submit"
          className="rounded-md bg-teal-800 px-3 py-2 text-sm font-medium text-white hover:bg-teal-900"
        >
          Apply filters
        </button>
        <button
          type="button"
          onClick={onClear}
          className="rounded-md px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100"
        >
          Clear
        </button>
      </div>
    </form>
  );
}

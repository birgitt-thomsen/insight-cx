import { Card, SectionHeader } from "../../components";
import type { ExecutiveFocusItem } from "../../types/executiveSummary";

export function ExecutiveSummarySection({
  summary,
  focus,
  priorityCounts,
}: {
  summary: string;
  focus: ExecutiveFocusItem[];
  priorityCounts: Record<string, number>;
}) {
  return (
    <section>
      <SectionHeader title="Executive Summary" subtitle="What leadership needs to know right now." />
      <Card className="p-6">
        <p className="text-sm leading-relaxed text-slate-700">{summary}</p>
      </Card>

      {focus.length > 0 && (
        <div className="mt-4 grid gap-4 sm:grid-cols-3">
          {focus.map((item, index) => {
            const count = priorityCounts[item.priority];
            return (
              <Card key={item.priority} className="p-5">
                <div className="flex items-start justify-between gap-2">
                  <p className="text-xs font-semibold uppercase tracking-wide text-indigo-600">
                    Focus {index + 1}
                  </p>
                  {Boolean(count) && (
                    <span className="whitespace-nowrap rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-700">
                      {count} {count === 1 ? "initiative" : "initiatives"}
                    </span>
                  )}
                </div>
                <h3 className="mt-2 text-sm font-semibold text-slate-900">{item.priority}</h3>
                <p className="mt-1 text-sm text-slate-600">{item.why_it_matters}</p>
              </Card>
            );
          })}
        </div>
      )}
    </section>
  );
}

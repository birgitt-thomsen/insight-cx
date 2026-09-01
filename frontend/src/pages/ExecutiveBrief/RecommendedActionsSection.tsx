import { Card, PriorityBadge, SectionHeader } from "../../components";
import type { RecommendedAction } from "../../types/executiveSummary";

export function RecommendedActionsSection({ actions }: { actions: RecommendedAction[] }) {
  if (actions.length === 0) return null;

  return (
    <section>
      <SectionHeader
        title="Recommended Actions"
        subtitle="Prioritized initiatives designed to address the highest-impact customer issues."
      />
      <div className="grid gap-4 lg:grid-cols-2">
        {actions.map((action) => (
          <Card key={action.action} className="flex flex-col p-5">
            <div className="flex items-start justify-between gap-3">
              <h3 className="text-sm font-semibold text-slate-900">{action.action}</h3>
              <PriorityBadge priority={action.priority} />
            </div>
            <p className="mt-2 text-sm text-slate-600">{action.details}</p>

            <dl className="mt-3 grid grid-cols-2 gap-3 text-xs text-slate-500">
              <div>
                <dt className="font-semibold uppercase tracking-wide">Owner</dt>
                <dd className="mt-0.5 text-slate-700">{action.owner}</dd>
              </div>
              <div>
                <dt className="font-semibold uppercase tracking-wide">Timeframe</dt>
                <dd className="mt-0.5 text-slate-700">{action.timeframe}</dd>
              </div>
            </dl>

            {action.supports_priority.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-1.5">
                {action.supports_priority.map((priority) => (
                  <span
                    key={priority}
                    className="rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-700"
                  >
                    {priority}
                  </span>
                ))}
              </div>
            )}

            <p className="mt-3 border-t border-slate-100 pt-3 text-xs text-slate-500">
              <span className="font-semibold uppercase tracking-wide text-slate-400">
                Success Measure
              </span>{" "}
              {action.success_measure}
            </p>
          </Card>
        ))}
      </div>
    </section>
  );
}

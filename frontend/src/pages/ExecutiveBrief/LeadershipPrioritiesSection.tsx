import { Card, SectionHeader } from "../../components";
import type { LeadershipPriority } from "../../types/executiveSummary";

export function LeadershipPrioritiesSection({ priorities }: { priorities: LeadershipPriority[] }) {
  if (priorities.length === 0) return null;

  return (
    <section>
      <SectionHeader
        title="Leadership Priorities"
        subtitle="The strategic issues leadership should prioritize based on business impact and customer experience."
      />
      <div className="space-y-4">
        {priorities.map((item) => (
          <Card key={item.strategic_priority} className="p-5">
            <h3 className="text-sm font-semibold text-slate-900">{item.strategic_priority}</h3>
            <div className="mt-3 grid gap-4 sm:grid-cols-2">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Business Objective
                </p>
                <p className="mt-1 text-sm text-slate-700">{item.business_objective}</p>
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Why Now</p>
                <p className="mt-1 text-sm text-slate-700">{item.why_now}</p>
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Expected Business Value
                </p>
                <p className="mt-1 text-sm text-slate-700">{item.expected_business_value}</p>
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                  Executive Owner
                </p>
                <p className="mt-1 text-sm font-medium text-indigo-700">{item.executive_owner}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </section>
  );
}

import { AlertTriangle, Sparkles, TrendingUp } from "lucide-react";
import { Card, ConfidenceBadge, SectionHeader } from "../../components";
import type { AiRootCauseFinding, EmergingBusinessSignal } from "../../types/executiveSummary";

const SIGNAL_ICON = { Risk: AlertTriangle, Opportunity: TrendingUp, Trend: Sparkles } as const;

const SEVERITY_CLASSES: Record<string, string> = {
  High: "bg-rose-50 text-rose-700 ring-rose-600/20",
  Medium: "bg-amber-50 text-amber-700 ring-amber-600/20",
  Low: "bg-emerald-50 text-emerald-700 ring-emerald-600/20",
};

export function AiInvestigationSection({
  findings,
  signals,
}: {
  findings: AiRootCauseFinding[];
  signals: EmergingBusinessSignal[];
}) {
  if (findings.length === 0 && signals.length === 0) return null;

  return (
    <section>
      <SectionHeader
        title="AI Investigation"
        subtitle="AI-generated hypotheses and early signals worth monitoring, with supporting customer evidence."
      />
      <div className="grid gap-6 lg:grid-cols-2">
        {findings.length > 0 && (
          <div className="space-y-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              Root Cause Analysis
            </p>
            {findings.map((finding) => (
              <Card key={finding.hypothesis} className="p-5">
                <div className="flex items-start justify-between gap-3">
                  <h3 className="text-sm font-semibold text-slate-900">{finding.hypothesis}</h3>
                  <ConfidenceBadge level={finding.confidence.level} />
                </div>
                <p className="mt-2 text-sm text-slate-600">{finding.summary}</p>

                <ul className="mt-3 space-y-1 text-sm text-slate-600">
                  {finding.evidence.map((item) => (
                    <li key={item} className="flex gap-2">
                      <span className="text-emerald-600" aria-hidden="true">
                        ✓
                      </span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>

                <div className="mt-3 space-y-2 border-t border-slate-100 pt-3 text-xs text-slate-500">
                  <p>
                    <span className="font-semibold uppercase tracking-wide text-slate-400">
                      Business Risk
                    </span>{" "}
                    {finding.business_risk}
                  </p>
                  <p>
                    <span className="font-semibold uppercase tracking-wide text-slate-400">
                      Recommended Validation
                    </span>{" "}
                    {finding.recommended_validation}
                  </p>
                </div>
              </Card>
            ))}
          </div>
        )}

        {signals.length > 0 && (
          <div className="space-y-4">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
              Emerging Business Signals
            </p>
            {signals.map((signal) => {
              const Icon = SIGNAL_ICON[signal.signal_type];
              return (
                <Card key={signal.business_signal} className="p-5">
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex items-start gap-2">
                      <Icon className="mt-0.5 h-4 w-4 shrink-0 text-slate-400" aria-hidden="true" />
                      <h3 className="text-sm font-semibold text-slate-900">{signal.business_signal}</h3>
                    </div>
                    <span
                      className={`whitespace-nowrap rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${
                        SEVERITY_CLASSES[signal.severity] ?? SEVERITY_CLASSES.Medium
                      }`}
                    >
                      {signal.severity}
                    </span>
                  </div>
                  <p className="mt-2 text-sm text-slate-600">{signal.description}</p>
                  <p className="mt-2 text-xs text-slate-500">
                    <span className="font-semibold uppercase tracking-wide text-slate-400">
                      Likelihood
                    </span>{" "}
                    {signal.likelihood}
                  </p>
                  <p className="mt-2 text-xs text-slate-500">
                    <span className="font-semibold uppercase tracking-wide text-slate-400">
                      Leadership Monitoring
                    </span>{" "}
                    {signal.recommended_monitoring}
                  </p>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </section>
  );
}

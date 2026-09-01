import { Card, MetricCard, SectionHeader } from "../../components";
import type { ExecutiveSummary } from "../../types/executiveSummary";
import { diffTrend } from "../../lib/trend";

export function KeyMetricsSection({
  current,
  previous,
}: {
  current: ExecutiveSummary;
  previous?: ExecutiveSummary;
}) {
  const npsScore = Math.round(
    current.nps_insight.promoter_percentage - current.nps_insight.detractor_percentage,
  );
  const previousNpsScore = previous
    ? Math.round(previous.nps_insight.promoter_percentage - previous.nps_insight.detractor_percentage)
    : undefined;

  return (
    <section>
      <SectionHeader title="Key Metrics" subtitle="The numbers behind the interpretation above." />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <MetricCard
          label="Total Feedback"
          value={current.key_metrics.feedback_count.toLocaleString()}
          helper="Responses analyzed in this period"
        />
        <MetricCard
          label="NPS"
          value={String(npsScore)}
          helper={`${current.nps_insight.promoter_percentage.toFixed(0)}% promoters · ${current.nps_insight.detractor_percentage.toFixed(0)}% detractors`}
          trend={diffTrend(npsScore, previousNpsScore, { goodDirection: "up" })}
        />
        <MetricCard
          label="CSAT"
          value={`${current.csat_insight.satisfied_percentage.toFixed(0)}%`}
          helper="Satisfied customers"
          trend={diffTrend(
            current.csat_insight.satisfied_percentage,
            previous?.csat_insight.satisfied_percentage,
            { goodDirection: "up" },
          )}
        />
        <MetricCard
          label="Confidence"
          value={`${current.confidence.score.toFixed(0)}%`}
          helper={current.confidence.level}
        />
      </div>

      <div className="mt-4 grid gap-4 sm:grid-cols-2">
        <Card className="p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">NPS Insight</p>
          <p className="mt-2 text-sm text-slate-700">{current.nps_insight.interpretation}</p>
          <p className="mt-2 text-sm font-medium text-indigo-700">
            {current.nps_insight.recommended_follow_up}
          </p>
        </Card>
        <Card className="p-5">
          <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">CSAT Insight</p>
          <p className="mt-2 text-sm text-slate-700">{current.csat_insight.interpretation}</p>
          <p className="mt-2 text-sm font-medium text-indigo-700">
            {current.csat_insight.recommended_follow_up}
          </p>
        </Card>
      </div>
    </section>
  );
}

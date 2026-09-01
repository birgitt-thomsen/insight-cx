import { Card, SectionHeader } from "../../components";
import type { BusinessDriver } from "../../types/executiveSummary";
import { driverTrendGlyph } from "../../lib/trendLabels";

export function BusinessDriversSection({
  drivers,
  totalFeedback,
}: {
  drivers: BusinessDriver[];
  totalFeedback: number;
}) {
  if (drivers.length === 0) return null;

  return (
    <section>
      <SectionHeader
        title="Business Drivers"
        subtitle="The recurring customer experiences that provide the factual foundation for this brief."
      />
      <div className="grid gap-4 sm:grid-cols-2">
        {drivers.map((driver) => {
          const trend = driverTrendGlyph(driver.period_comparison.trend);
          const share = totalFeedback > 0 ? Math.round((driver.count / totalFeedback) * 100) : null;

          return (
            <Card key={driver.driver} className="p-5">
              <div className="flex items-start justify-between gap-3">
                <h3 className="text-sm font-semibold text-slate-900">{driver.driver}</h3>
                <span className="whitespace-nowrap rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600">
                  {driver.count} {driver.count === 1 ? "record" : "records"}
                  {share !== null && ` · ${share}%`}
                </span>
              </div>
              <p className="mt-2 text-sm text-slate-600">{driver.summary}</p>
              {driver.period_comparison.summary && (
                <p className={`mt-3 flex items-start gap-2 text-xs font-medium ${trend.toneClass}`}>
                  <span aria-hidden="true">{trend.icon}</span>
                  <span>
                    {trend.label}: {driver.period_comparison.summary}
                  </span>
                </p>
              )}
            </Card>
          );
        })}
      </div>
    </section>
  );
}

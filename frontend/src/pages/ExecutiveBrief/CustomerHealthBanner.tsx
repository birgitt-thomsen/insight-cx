import type { CustomerHealth } from "../../types/executiveSummary";
import { healthTrendGlyph } from "../../lib/trendLabels";

const TONE_CLASSES: Record<string, { bg: string; text: string; badge: string }> = {
  green: {
    bg: "bg-emerald-50 border-emerald-200",
    text: "text-emerald-900",
    badge: "bg-emerald-600 text-white",
  },
  amber: {
    bg: "bg-amber-50 border-amber-200",
    text: "text-amber-900",
    badge: "bg-amber-600 text-white",
  },
  red: {
    bg: "bg-rose-50 border-rose-200",
    text: "text-rose-900",
    badge: "bg-rose-600 text-white",
  },
};

export function CustomerHealthBanner({
  health,
  businessImpact,
}: {
  health: CustomerHealth;
  businessImpact: string;
}) {
  const tone = TONE_CLASSES[health.color] ?? TONE_CLASSES.amber;
  const trend = healthTrendGlyph(health.period_comparison.trend);

  return (
    <section className={`rounded-xl border p-6 sm:p-8 ${tone.bg}`}>
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start">
        <span
          className={`inline-flex shrink-0 items-center rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide ${tone.badge}`}
        >
          {health.status}
        </span>
        <div className={`flex-1 ${tone.text}`}>
          <h2 className="text-xl font-semibold">{health.headline}</h2>
          <p className="mt-2 text-sm">{businessImpact}</p>
          {health.period_comparison.summary && (
            <p className={`mt-3 flex items-start gap-2 text-sm font-medium ${trend.toneClass}`}>
              <span aria-hidden="true">{trend.icon}</span>
              <span>{health.period_comparison.summary}</span>
            </p>
          )}
        </div>
      </div>
    </section>
  );
}

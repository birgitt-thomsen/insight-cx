import { Card } from "./Card";

export interface MetricCardTrend {
  direction: "up" | "down" | "stable";
  label: string;
  /** Positive framing overrides color: an "up" trend is not always good (e.g. negative sentiment share). */
  tone?: "positive" | "negative" | "neutral";
}

export function MetricCard({
  label,
  value,
  helper,
  trend,
}: {
  label: string;
  value: string;
  helper?: string;
  trend?: MetricCardTrend;
}) {
  const trendColor =
    trend?.tone === "negative"
      ? "text-rose-600"
      : trend?.tone === "positive"
        ? "text-emerald-600"
        : trend?.direction === "up"
          ? "text-emerald-600"
          : trend?.direction === "down"
            ? "text-rose-600"
            : "text-slate-500";

  const trendGlyph =
    trend?.direction === "up" ? "▲" : trend?.direction === "down" ? "▼" : "●";

  return (
    <Card className="p-5">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-slate-900">{value}</p>
      {helper && <p className="mt-1 text-xs text-slate-500">{helper}</p>}
      {trend && (
        <p className={`mt-2 text-xs font-medium ${trendColor}`}>
          {trendGlyph} {trend.label}
        </p>
      )}
    </Card>
  );
}

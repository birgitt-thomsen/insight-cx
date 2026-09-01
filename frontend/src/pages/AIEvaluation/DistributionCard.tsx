import { Card } from "../../components";

export function DistributionCard({
  title,
  columnLabel = "Value",
  entries,
}: {
  title: string;
  columnLabel?: string;
  entries: [string, number][];
}) {
  const sorted = [...entries].sort((a, b) => b[1] - a[1]);

  return (
    <Card className="p-4">
      <h4 className="text-base font-semibold text-slate-900">{title}</h4>
      {sorted.length === 0 ? (
        <p className="mt-2 text-sm text-slate-400">No data.</p>
      ) : (
        <div className="mt-3">
          <div className="flex items-center justify-between border-b border-slate-200 pb-1.5 text-xs font-semibold uppercase tracking-wide text-slate-400">
            <span>{columnLabel}</span>
            <span>Count</span>
          </div>
          <ul className="divide-y divide-slate-100">
            {sorted.map(([label, count]) => (
              <li key={label} className="flex items-center justify-between gap-2 py-1.5 text-sm">
                <span className="text-slate-600">{label}</span>
                <span className="font-semibold text-slate-800">{count}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </Card>
  );
}

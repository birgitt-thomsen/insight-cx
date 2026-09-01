import type { ReactNode } from "react";
import { Card, PriorityBadge, SentimentBadge } from "../../components";
import type { Analysis } from "../../types/feedback";
import type { AiOutputAnalysis } from "../../types/aiEvaluation";

function NotAnalyzed() {
  return <span className="text-sm text-slate-400">Not yet analyzed</span>;
}

function TagList({ items, tone }: { items: string[]; tone: "slate" | "indigo" }) {
  if (items.length === 0) return <span className="text-sm text-slate-400">—</span>;

  const toneClass = tone === "indigo" ? "bg-indigo-50 text-indigo-700" : "bg-slate-100 text-slate-600";

  return (
    <div className="flex flex-wrap gap-1.5">
      {items.map((item) => (
        <span key={item} className={`rounded-full px-2 py-0.5 text-xs font-medium ${toneClass}`}>
          {item}
        </span>
      ))}
    </div>
  );
}

function ComparisonCard({
  title,
  changed,
  wide,
  children,
}: {
  title: string;
  changed: boolean;
  wide?: boolean;
  children: ReactNode;
}) {
  return (
    <Card className={`p-4 ${changed ? "ring-2 ring-indigo-300" : ""} ${wide ? "sm:col-span-2" : ""}`}>
      <div className="flex items-center justify-between gap-2">
        <h4 className="text-sm font-semibold text-slate-900">{title}</h4>
        {changed && (
          <span className="whitespace-nowrap rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-700">
            ✓ Changed
          </span>
        )}
      </div>
      {children}
    </Card>
  );
}

function CompareColumns({ current, next }: { current: ReactNode; next: ReactNode }) {
  return (
    <div className="mt-2 grid grid-cols-1 gap-3 sm:grid-cols-2">
      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Current</p>
        <div className="mt-1 text-sm text-slate-700">{current}</div>
      </div>
      <div>
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">New</p>
        <div className="mt-1 text-sm text-slate-700">{next}</div>
      </div>
    </div>
  );
}

function sortedReasonCodes(reasonCodes: Analysis["reason_codes"]) {
  return [...(reasonCodes ?? [])].sort((a, b) => a.rank - b.rank);
}

export function AnalysisComparisonGrid({
  current,
  output,
  changedFields,
}: {
  current: Analysis | null;
  output: AiOutputAnalysis;
  changedFields: string[];
}) {
  const isChanged = (field: string) => changedFields.includes(field);

  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <ComparisonCard title="Sentiment" changed={isChanged("sentiment")}>
        <CompareColumns
          current={current ? <SentimentBadge sentiment={current.sentiment} /> : <NotAnalyzed />}
          next={<SentimentBadge sentiment={output.sentiment} />}
        />
      </ComparisonCard>

      <ComparisonCard title="Priority" changed={isChanged("priority")}>
        <CompareColumns
          current={current ? <PriorityBadge priority={current.priority} /> : <NotAnalyzed />}
          next={<PriorityBadge priority={output.priority} />}
        />
      </ComparisonCard>

      <ComparisonCard title="Emotions" changed={isChanged("emotions")} wide>
        <CompareColumns
          current={current?.emotions?.length ? <TagList items={current.emotions} tone="slate" /> : <NotAnalyzed />}
          next={<TagList items={output.emotions} tone="slate" />}
        />
      </ComparisonCard>

      <ComparisonCard title="Customer Intent" changed={isChanged("intent")} wide>
        <CompareColumns
          current={current?.intent?.length ? <TagList items={current.intent} tone="indigo" /> : <NotAnalyzed />}
          next={<TagList items={output.intent} tone="indigo" />}
        />
      </ComparisonCard>

      <ComparisonCard title="Confidence" changed={isChanged("confidence")} wide>
        <CompareColumns
          current={
            current ? (
              `${current.confidence_level ?? "—"} (${current.confidence_score ?? "—"}%)`
            ) : (
              <NotAnalyzed />
            )
          }
          next={
            <>
              {output.confidence.level} ({output.confidence.score}%)
              <p className="mt-1 text-xs text-slate-500">{output.confidence.reason}</p>
            </>
          }
        />
      </ComparisonCard>

      <ComparisonCard title="Reason Codes" changed={isChanged("reason_codes")} wide>
        <CompareColumns
          current={
            current?.reason_codes?.length ? (
              <ol className="space-y-0.5">
                {sortedReasonCodes(current.reason_codes).map((reason) => (
                  <li key={reason.code}>
                    {reason.rank}. {reason.code}
                  </li>
                ))}
              </ol>
            ) : (
              <NotAnalyzed />
            )
          }
          next={
            <ol className="space-y-0.5">
              {sortedReasonCodes(output.reason_codes).map((reason) => (
                <li key={reason.code}>
                  {reason.rank}. {reason.code}
                </li>
              ))}
            </ol>
          }
        />
      </ComparisonCard>

      <ComparisonCard title="Business Signal" changed={isChanged("business_signal")} wide>
        <CompareColumns
          current={current?.business_signal ?? <NotAnalyzed />}
          next={output.business_signal}
        />
      </ComparisonCard>
    </div>
  );
}

import { Card, SectionHeader } from "../../components";
import type { EmotionSummaryItem, IntentSummary, SentimentSummary } from "../../types/executiveSummary";
import { formatPercent } from "../../lib/format";

function MiniStat({ label, value, toneClass }: { label: string; value: number; toneClass: string }) {
  return (
    <div className={`rounded-lg border p-4 text-center ${toneClass}`}>
      <p className="text-2xl font-semibold">{formatPercent(value)}</p>
      <p className="mt-1 text-xs font-medium uppercase tracking-wide">{label}</p>
    </div>
  );
}

export function SentimentEmotionIntentSection({
  sentiment,
  emotions,
  intent,
}: {
  sentiment: SentimentSummary;
  emotions: EmotionSummaryItem[];
  intent: IntentSummary;
}) {
  return (
    <section>
      <SectionHeader
        title="Sentiment, Emotion & Intent"
        subtitle="What customers are feeling, and what they intend to do next."
      />
      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="p-5">
          <h3 className="text-sm font-semibold text-slate-900">Customer Sentiment</h3>
          <p className="mt-1 text-sm text-slate-600">{sentiment.insight}</p>
          <div className="mt-4 grid grid-cols-3 gap-3">
            <MiniStat
              label="Positive"
              value={sentiment.positive_percentage}
              toneClass="border-emerald-200 bg-emerald-50 text-emerald-700"
            />
            <MiniStat
              label="Neutral"
              value={sentiment.neutral_percentage}
              toneClass="border-slate-200 bg-slate-50 text-slate-600"
            />
            <MiniStat
              label="Negative"
              value={sentiment.negative_percentage}
              toneClass="border-rose-200 bg-rose-50 text-rose-700"
            />
          </div>

          {emotions.length > 0 && (
            <div className="mt-5 space-y-3 border-t border-slate-100 pt-4">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                Dominant Emotions
              </p>
              {emotions.map((emotion) => (
                <div key={emotion.emotion}>
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium text-slate-700">{emotion.emotion}</span>
                    <span className="text-slate-500">{formatPercent(emotion.percentage)}</span>
                  </div>
                  <p className="mt-0.5 text-xs text-slate-500">{emotion.business_meaning}</p>
                </div>
              ))}
            </div>
          )}
        </Card>

        <Card className="p-5">
          <h3 className="text-sm font-semibold text-slate-900">{intent.headline}</h3>
          <p className="mt-1 text-sm text-slate-600">{intent.insight}</p>

          {intent.top_intents.length > 0 && (
            <div className="mt-4 space-y-3 border-t border-slate-100 pt-4">
              {intent.top_intents.map((item) => (
                <div key={item.intent}>
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium text-slate-700">{item.intent}</span>
                    <span className="text-slate-500">{formatPercent(item.percentage)}</span>
                  </div>
                  <p className="mt-0.5 text-xs text-slate-500">{item.business_meaning}</p>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>
    </section>
  );
}

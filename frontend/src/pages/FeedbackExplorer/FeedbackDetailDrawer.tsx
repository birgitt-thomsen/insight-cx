import { Link } from "react-router-dom";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { fetchFeedbackDetail, reanalyzeFeedback } from "../../api/feedback";
import {
  ConfidenceBadge,
  Drawer,
  EmptyState,
  ErrorState,
  LoadingState,
  PriorityBadge,
  SentimentBadge,
} from "../../components";
import { formatDate, formatDateTime } from "../../lib/format";

export function FeedbackDetailDrawer({
  feedbackId,
  onClose,
}: {
  feedbackId: number;
  onClose: () => void;
}) {
  const queryClient = useQueryClient();

  const {
    data: feedback,
    isLoading,
    isError,
    error,
    refetch,
  } = useQuery({
    queryKey: ["feedback", "detail", feedbackId],
    queryFn: () => fetchFeedbackDetail(feedbackId),
  });

  const reanalyzeMutation = useMutation({
    mutationFn: () => reanalyzeFeedback(feedbackId),
    onSuccess: (updated) => {
      queryClient.setQueryData(["feedback", "detail", feedbackId], updated);
      queryClient.invalidateQueries({ queryKey: ["feedback"], exact: false });
    },
  });

  const analysis = feedback?.analysis;

  return (
    <Drawer open onClose={onClose} title="Customer Feedback">
      {isLoading && <LoadingState label="Loading feedback…" />}

      {isError && (
        <ErrorState
          description={
            error instanceof Error ? error.message : "Could not load this feedback record."
          }
          onRetry={() => refetch()}
        />
      )}

      {feedback && (
        <div className="space-y-6">
          <blockquote className="rounded-lg bg-slate-50 p-4 text-sm italic text-slate-700">
            “{feedback.comment}”
          </blockquote>

          <dl className="grid grid-cols-1 gap-4 text-sm sm:grid-cols-2">
            <div>
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-400">Customer</dt>
              <dd className="mt-0.5 text-slate-700">{feedback.customer_name}</dd>
            </div>
            <div>
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                Customer ID
              </dt>
              <dd className="mt-0.5 text-slate-700">{feedback.customer_id}</dd>
            </div>
            <div>
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-400">Order</dt>
              <dd className="mt-0.5 text-slate-700">{feedback.order_number}</dd>
            </div>
            <div>
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                Feedback Date
              </dt>
              <dd className="mt-0.5 text-slate-700">{formatDate(feedback.feedback_date)}</dd>
            </div>
            <div>
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-400">Survey</dt>
              <dd className="mt-0.5 text-slate-700">
                {feedback.survey_type} · Score {feedback.score}
              </dd>
            </div>
            <div>
              <dt className="text-xs font-semibold uppercase tracking-wide text-slate-400">Source</dt>
              <dd className="mt-0.5 text-slate-700">{feedback.source ?? "—"}</dd>
            </div>
          </dl>

          <div className="border-t border-slate-200 pt-5">
            <h3 className="text-sm font-semibold text-slate-900">AI Assessment</h3>

            {!analysis ? (
              <EmptyState
                title="Not yet analyzed"
                description="This feedback hasn't been through AI analysis yet."
              />
            ) : (
              <div className="mt-3 space-y-4">
                <div className="flex flex-wrap gap-2">
                  <SentimentBadge sentiment={analysis.sentiment} />
                  <PriorityBadge priority={analysis.priority} />
                  <ConfidenceBadge level={analysis.confidence_level} />
                </div>

                {analysis.emotions && analysis.emotions.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      Emotions
                    </p>
                    <div className="mt-1 flex flex-wrap gap-1.5">
                      {analysis.emotions.map((emotion) => (
                        <span
                          key={emotion}
                          className="rounded-full bg-slate-100 px-2 py-0.5 text-xs font-medium text-slate-600"
                        >
                          {emotion}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {analysis.intent && analysis.intent.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      Customer Intent
                    </p>
                    <div className="mt-1 flex flex-wrap gap-1.5">
                      {analysis.intent.map((intent) => (
                        <span
                          key={intent}
                          className="rounded-full bg-indigo-50 px-2 py-0.5 text-xs font-medium text-indigo-700"
                        >
                          {intent}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {analysis.reason_codes && analysis.reason_codes.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      Reason Codes
                    </p>
                    <ol className="mt-1 space-y-1 text-sm text-slate-700">
                      {[...analysis.reason_codes]
                        .sort((a, b) => a.rank - b.rank)
                        .map((reason) => (
                          <li key={reason.code}>
                            {reason.rank}. {reason.code}
                          </li>
                        ))}
                    </ol>
                  </div>
                )}

                {analysis.business_signal && (
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      Business Interpretation
                    </p>
                    <p className="mt-1 text-sm text-slate-700">{analysis.business_signal}</p>
                  </div>
                )}

                <details className="rounded-lg border border-slate-200 bg-slate-50 p-3 text-xs text-slate-500">
                  <summary className="cursor-pointer font-medium text-slate-600">
                    Analysis metadata
                  </summary>
                  <dl className="mt-2 space-y-1">
                    <div className="flex justify-between gap-2">
                      <dt>Model</dt>
                      <dd>{analysis.model}</dd>
                    </div>
                    <div className="flex justify-between gap-2">
                      <dt>System Prompt</dt>
                      <dd>{analysis.system_prompt_version}</dd>
                    </div>
                    <div className="flex justify-between gap-2">
                      <dt>Feedback Prompt</dt>
                      <dd>{analysis.feedback_prompt_version}</dd>
                    </div>
                    <div className="flex justify-between gap-2">
                      <dt>Analysis Version</dt>
                      <dd>{analysis.analysis_version}</dd>
                    </div>
                    <div className="flex justify-between gap-2">
                      <dt>Analyzed</dt>
                      <dd>{formatDateTime(analysis.analyzed_at)}</dd>
                    </div>
                  </dl>
                </details>
              </div>
            )}
          </div>

          <div className="flex flex-wrap gap-2 border-t border-slate-200 pt-5">
            <button
              type="button"
              onClick={() => reanalyzeMutation.mutate()}
              disabled={reanalyzeMutation.isPending}
              className="rounded-md bg-teal-800 px-3 py-2 text-sm font-medium text-white hover:bg-teal-900 disabled:opacity-50"
            >
              {reanalyzeMutation.isPending ? "Re-analyzing…" : "Re-analyze Feedback"}
            </button>
            <Link
              to={`/ai-evaluation?feedback_id=${feedback.id}`}
              className="rounded-md px-3 py-2 text-sm font-medium text-slate-600 ring-1 ring-inset ring-slate-300 hover:bg-slate-100"
            >
              Test in AI Evaluation
            </Link>
          </div>

          {reanalyzeMutation.isError && (
            <p className="text-sm text-rose-600">
              {reanalyzeMutation.error instanceof Error
                ? reanalyzeMutation.error.message
                : "Re-analysis failed."}
            </p>
          )}
        </div>
      )}
    </Drawer>
  );
}

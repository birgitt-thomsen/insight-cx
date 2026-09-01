import { useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { keepPreviousData, useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { MessageSquare } from "lucide-react";
import { fetchFeedbackPage, toggleSample } from "../../api/feedback";
import {
  Badge,
  Card,
  DataTable,
  EmptyState,
  ErrorState,
  LoadingState,
  PageHeader,
  PriorityBadge,
  SentimentBadge,
} from "../../components";
import type { DataTableColumn } from "../../components/DataTable";
import type { Feedback, FeedbackFilters } from "../../types/feedback";
import { formatDate } from "../../lib/format";
import { FeedbackFiltersBar } from "./FeedbackFiltersBar";
import { FeedbackDetailDrawer } from "./FeedbackDetailDrawer";

export default function FeedbackExplorer() {
  const [searchParams, setSearchParams] = useSearchParams();
  const [selectedFeedbackId, setSelectedFeedbackId] = useState<number | null>(null);
  const queryClient = useQueryClient();

  const page = Math.max(1, Number(searchParams.get("page") ?? "1") || 1);
  const filters: FeedbackFilters = {
    page,
    search: searchParams.get("search") ?? "",
    survey_type: searchParams.get("survey_type") ?? "",
    sentiment: searchParams.get("sentiment") ?? "",
    priority: searchParams.get("priority") ?? "",
  };

  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
    isFetching,
  } = useQuery({
    queryKey: ["feedback", filters],
    queryFn: () => fetchFeedbackPage(filters),
    placeholderData: keepPreviousData,
  });

  const toggleSampleMutation = useMutation({
    mutationFn: ({ id, selected }: { id: number; selected: boolean }) => toggleSample(id, selected),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["feedback"] });
    },
  });

  function updateFilters(next: Omit<FeedbackFilters, "page">) {
    const params = new URLSearchParams();
    if (next.search) params.set("search", next.search);
    if (next.survey_type) params.set("survey_type", next.survey_type);
    if (next.sentiment) params.set("sentiment", next.sentiment);
    if (next.priority) params.set("priority", next.priority);
    setSearchParams(params);
  }

  function goToPage(nextPage: number) {
    const params = new URLSearchParams(searchParams);
    params.set("page", String(nextPage));
    setSearchParams(params);
  }

  const columns: DataTableColumn<Feedback>[] = [
    {
      key: "sample",
      header: "Sample",
      render: (row) => (
        <input
          type="checkbox"
          checked={row.is_test_sample}
          disabled={toggleSampleMutation.isPending}
          onChange={(event) =>
            toggleSampleMutation.mutate({ id: row.id, selected: event.target.checked })
          }
          aria-label={`Include feedback from ${row.customer_name} in the AI Evaluation benchmark sample`}
          className="h-4 w-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
        />
      ),
    },
    { key: "date", header: "Date", render: (row) => formatDate(row.feedback_date) },
    {
      key: "customer",
      header: "Customer",
      render: (row) => <span className="font-medium text-slate-900">{row.customer_name}</span>,
    },
    { key: "survey", header: "Survey", render: (row) => <Badge>{row.survey_type}</Badge> },
    { key: "score", header: "Score", render: (row) => row.score },
    {
      key: "sentiment",
      header: "Sentiment",
      render: (row) =>
        row.analysis ? (
          <SentimentBadge sentiment={row.analysis.sentiment} />
        ) : (
          <Badge className="bg-slate-100 text-slate-500 ring-slate-500/20">Pending</Badge>
        ),
    },
    {
      key: "priority",
      header: "Priority",
      render: (row) =>
        row.analysis ? (
          <PriorityBadge priority={row.analysis.priority} />
        ) : (
          <Badge className="bg-slate-100 text-slate-500 ring-slate-500/20">Pending</Badge>
        ),
    },
    {
      key: "comment",
      header: "Comment",
      className: "max-w-sm",
      render: (row) => <p className="line-clamp-2 text-slate-600">{row.comment}</p>,
    },
    {
      key: "details",
      header: "Details",
      render: (row) => (
        <button
          type="button"
          onClick={() => setSelectedFeedbackId(row.id)}
          className="font-medium text-teal-800 hover:text-teal-900"
        >
          View →
        </button>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title="Feedback Explorer"
        subtitle="Search, filter and review individual customer feedback with AI-generated analysis."
      />

      <Card className="p-5">
        <FeedbackFiltersBar
          filters={filters}
          surveyTypes={data?.survey_types ?? []}
          onApply={updateFilters}
          onClear={() => setSearchParams({})}
        />
      </Card>

      <div className="mt-6 space-y-6">
        {isLoading && <LoadingState label="Loading feedback…" />}

        {isError && (
          <ErrorState
            description={
              error instanceof Error ? error.message : "Could not reach the InsightCX backend."
            }
            onRetry={() => refetch()}
          />
        )}

        {!isLoading && !isError && data && (
          <>
            <Card className={`p-5 ${isFetching ? "opacity-70" : ""}`}>
              <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
                <h2 className="text-lg font-semibold text-slate-900">Feedback Results</h2>
                <p className="text-sm text-slate-500">
                  Showing {data.items.length} of {data.total} matching{" "}
                  {data.total === 1 ? "record" : "records"}
                </p>
              </div>

              {data.items.length === 0 ? (
                <EmptyState
                  icon={<MessageSquare className="h-8 w-8" aria-hidden="true" />}
                  title="No feedback matches these filters"
                  description="Try clearing one or more filters, or check back after the next CSV import."
                />
              ) : (
                <DataTable columns={columns} rows={data.items} rowKey={(row) => row.id} />
              )}

              <div className="mt-4 flex items-center justify-between text-sm text-slate-500">
                <button
                  type="button"
                  disabled={!data.has_prev}
                  onClick={() => goToPage(page - 1)}
                  className="rounded-md px-3 py-1.5 font-medium text-slate-600 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  ← Previous
                </button>
                <span>
                  Page {data.page} of {Math.max(data.pages, 1)}
                </span>
                <button
                  type="button"
                  disabled={!data.has_next}
                  onClick={() => goToPage(page + 1)}
                  className="rounded-md px-3 py-1.5 font-medium text-slate-600 hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
                >
                  Next →
                </button>
              </div>
            </Card>

            <Card className="flex flex-wrap items-center justify-between gap-3 p-5">
              <div>
                <p className="text-sm font-semibold text-slate-900">AI Evaluation Benchmark Sample</p>
                <p className="text-sm text-slate-500">
                  {data.sample_count} {data.sample_count === 1 ? "record" : "records"} selected using
                  the Sample column above.
                </p>
              </div>
              <Link
                to="/ai-evaluation?tab=benchmark"
                className="rounded-md bg-teal-800 px-3 py-2 text-sm font-medium text-white hover:bg-teal-900"
              >
                Open Benchmark Lab →
              </Link>
            </Card>
          </>
        )}
      </div>

      {selectedFeedbackId !== null && (
        <FeedbackDetailDrawer
          feedbackId={selectedFeedbackId}
          onClose={() => setSelectedFeedbackId(null)}
        />
      )}
    </div>
  );
}

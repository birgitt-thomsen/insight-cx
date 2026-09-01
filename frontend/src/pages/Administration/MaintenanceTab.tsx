import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { deleteAllAnalyses, deleteAllFeedback, reanalyzeAllFeedback } from "../../api/maintenance";
import { Card, ConfirmationDialog } from "../../components";

type ConfirmAction = "reanalyze" | "delete-analyses" | "delete-feedback" | null;

export function MaintenanceTab() {
  const queryClient = useQueryClient();
  const [confirmAction, setConfirmAction] = useState<ConfirmAction>(null);
  const [resultMessage, setResultMessage] = useState<string | null>(null);

  function invalidateAffectedData() {
    queryClient.invalidateQueries({ queryKey: ["feedback"] });
    queryClient.invalidateQueries({ queryKey: ["executive-summary"] });
  }

  const reanalyzeMutation = useMutation({
    mutationFn: reanalyzeAllFeedback,
    onSuccess: (result) => {
      setResultMessage(`Re-analysis complete. ${result.processed} processed, ${result.failed} failed.`);
      invalidateAffectedData();
      setConfirmAction(null);
    },
  });

  const deleteAnalysesMutation = useMutation({
    mutationFn: deleteAllAnalyses,
    onSuccess: () => {
      setResultMessage("All analyses deleted. Raw feedback was preserved.");
      invalidateAffectedData();
      setConfirmAction(null);
    },
  });

  const deleteFeedbackMutation = useMutation({
    mutationFn: deleteAllFeedback,
    onSuccess: () => {
      setResultMessage("All feedback and analyses deleted.");
      invalidateAffectedData();
      setConfirmAction(null);
    },
  });

  const anyPending =
    reanalyzeMutation.isPending || deleteAnalysesMutation.isPending || deleteFeedbackMutation.isPending;

  return (
    <div className="space-y-6">
      {resultMessage && (
        <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">
          {resultMessage}
        </div>
      )}

      <Card className="p-5">
        <h3 className="text-sm font-semibold text-slate-900">Re-analyze All Feedback</h3>
        <p className="mt-1 text-sm text-slate-500">
          Re-runs the current feedback prompt across every stored record. Existing analyses are
          replaced when the run completes.
        </p>
        <button
          type="button"
          onClick={() => setConfirmAction("reanalyze")}
          disabled={anyPending}
          className="mt-4 rounded-md bg-teal-800 px-4 py-2 text-sm font-medium text-white hover:bg-teal-900 disabled:opacity-50"
        >
          Re-analyze All
        </button>
      </Card>

      <Card className="border-rose-200 bg-rose-50/40 p-5">
        <div className="flex items-start gap-2">
          <span className="text-lg text-rose-500" aria-hidden="true">
            ⚠
          </span>
          <div>
            <h3 className="text-sm font-semibold text-rose-700">Danger Zone</h3>
            <p className="mt-1 text-sm text-rose-600">
              These operations permanently remove data from the InsightCX database and cannot be
              undone. Confirmation is required for each action.
            </p>
          </div>
        </div>

        <div className="mt-4 space-y-4">
          <div className="grid grid-cols-1 items-center gap-4 rounded-lg border border-rose-200 bg-white p-4 sm:grid-cols-[1fr_auto]">
            <div>
              <p className="text-sm font-semibold text-slate-900">Delete All Analyses</p>
              <p className="mt-1 text-sm text-slate-500">
                Removes every AI analysis while keeping the raw feedback. The Executive Brief will be
                empty until a re-analysis is run.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setConfirmAction("delete-analyses")}
              disabled={anyPending}
              className="whitespace-nowrap rounded-md bg-rose-600 px-4 py-2 text-sm font-medium text-white hover:bg-rose-700 disabled:opacity-50"
            >
              Delete All Analyses
            </button>
          </div>

          <div className="grid grid-cols-1 items-center gap-4 rounded-lg border border-rose-200 bg-white p-4 sm:grid-cols-[1fr_auto]">
            <div>
              <p className="text-sm font-semibold text-slate-900">Delete All Feedback</p>
              <p className="mt-1 text-sm text-slate-500">
                Removes every feedback record and its analysis. The Executive Brief, Feedback
                Explorer, and benchmarks will be empty until new data is imported.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setConfirmAction("delete-feedback")}
              disabled={anyPending}
              className="whitespace-nowrap rounded-md bg-rose-600 px-4 py-2 text-sm font-medium text-white hover:bg-rose-700 disabled:opacity-50"
            >
              Delete All Feedback
            </button>
          </div>
        </div>
      </Card>

      <ConfirmationDialog
        open={confirmAction === "reanalyze"}
        onClose={() => setConfirmAction(null)}
        onConfirm={() => reanalyzeMutation.mutate()}
        title="Re-analyze all feedback?"
        description="This replaces every stored analysis with a fresh run using the current feedback prompt configuration. This may take a while for larger datasets."
        confirmLabel="Re-analyze All"
        loading={reanalyzeMutation.isPending}
      />

      <ConfirmationDialog
        open={confirmAction === "delete-analyses"}
        onClose={() => setConfirmAction(null)}
        onConfirm={() => deleteAnalysesMutation.mutate()}
        title="Delete all analyses?"
        description="Every AI analysis will be permanently deleted. Raw feedback records are kept and can be re-analyzed later."
        confirmLabel="Delete All Analyses"
        destructive
        loading={deleteAnalysesMutation.isPending}
      />

      <ConfirmationDialog
        open={confirmAction === "delete-feedback"}
        onClose={() => setConfirmAction(null)}
        onConfirm={() => deleteFeedbackMutation.mutate()}
        title="Delete all feedback?"
        description="Every feedback record and its analysis will be permanently deleted. This cannot be undone."
        confirmLabel="Delete All Feedback"
        destructive
        loading={deleteFeedbackMutation.isPending}
      />
    </div>
  );
}

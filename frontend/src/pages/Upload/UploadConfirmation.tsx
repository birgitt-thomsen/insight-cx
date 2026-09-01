import { Link } from "react-router-dom";
import { CheckCircle2 } from "lucide-react";
import type { UploadResult } from "../../api/upload";

export function UploadConfirmation({
  result,
  onUploadAnother,
}: {
  result: UploadResult;
  onUploadAnother: () => void;
}) {
  return (
    <div className="flex flex-col items-center gap-2 py-10 text-center">
      <CheckCircle2 className="h-10 w-10 text-emerald-600" aria-hidden="true" />
      <h2 className="text-lg font-semibold text-slate-900">Import complete</h2>
      <p className="max-w-md text-sm text-slate-600">
        Imported {result.imported.toLocaleString()} feedback{" "}
        {result.imported === 1 ? "record" : "records"}. Analyzed{" "}
        {result.processed.toLocaleString()} {result.processed === 1 ? "record" : "records"}
        {result.failed > 0 ? ` (${result.failed} failed).` : "."}
      </p>
      <div className="mt-4 flex gap-3">
        <button
          type="button"
          onClick={onUploadAnother}
          className="rounded-md px-3 py-2 text-sm font-medium text-slate-600 ring-1 ring-inset ring-slate-300 hover:bg-slate-100"
        >
          Upload Another File
        </button>
        <Link
          to="/feedback-explorer"
          className="rounded-md bg-teal-800 px-3 py-2 text-sm font-medium text-white hover:bg-teal-900"
        >
          View in Feedback Explorer
        </Link>
      </div>
    </div>
  );
}

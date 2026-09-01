import type { CsvPreviewResult } from "../../lib/csv";
import { MAX_CSV_ROWS } from "../../lib/csv";

export function UploadPreview({
  fileName,
  preview,
  isImporting,
  importError,
  onImport,
  onChooseDifferentFile,
}: {
  fileName: string;
  preview: CsvPreviewResult;
  isImporting: boolean;
  importError: string | null;
  onImport: () => void;
  onChooseDifferentFile: () => void;
}) {
  const exceedsLimit = preview.totalDataRows > MAX_CSV_ROWS;
  const hasNoRows = preview.totalDataRows === 0;
  const canImport = preview.missingColumns.length === 0 && !exceedsLimit && !hasNoRows;

  return (
    <div>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Preview {fileName}</h2>
          <p className="mt-1 text-sm text-slate-500">
            Detected {preview.headers.length} columns and {preview.totalDataRows.toLocaleString()} data{" "}
            {preview.totalDataRows === 1 ? "row" : "rows"}, using{" "}
            <span className="font-mono">{preview.delimiter === "," ? "comma" : "semicolon"}</span> as the
            delimiter. Showing the first {preview.rows.length} rows below.
          </p>
        </div>
        <button
          type="button"
          onClick={onChooseDifferentFile}
          className="rounded-md px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100"
        >
          Choose a different file
        </button>
      </div>

      {preview.missingColumns.length > 0 && (
        <div
          role="alert"
          className="mt-4 rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700"
        >
          <p className="font-semibold">This file is missing required columns.</p>
          <p className="mt-1">Missing: {preview.missingColumns.join(", ")}</p>
        </div>
      )}

      {exceedsLimit && (
        <div
          role="alert"
          className="mt-4 rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-700"
        >
          This file has {preview.totalDataRows.toLocaleString()} rows, which exceeds the{" "}
          {MAX_CSV_ROWS.toLocaleString()} record limit. Split it into smaller files before importing.
        </div>
      )}

      {hasNoRows && (
        <div
          role="alert"
          className="mt-4 rounded-lg border border-amber-200 bg-amber-50 p-4 text-sm text-amber-700"
        >
          This file only contains a header row. Add at least one feedback record before importing.
        </div>
      )}

      {importError && (
        <div
          role="alert"
          className="mt-4 rounded-lg border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700"
        >
          <p className="font-semibold">Import failed</p>
          <p className="mt-1">{importError}</p>
        </div>
      )}

      <div className="mt-4 overflow-x-auto rounded-lg border border-slate-200">
        <table className="w-full min-w-[720px] text-left text-sm">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50 text-xs font-medium uppercase tracking-wide text-slate-500">
              {preview.headers.map((header) => (
                <th key={header} className="whitespace-nowrap px-3 py-2">
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {preview.rows.map((row, index) => (
              <tr key={index}>
                {preview.headers.map((header, cellIndex) => (
                  <td key={header} className="whitespace-nowrap px-3 py-2 text-slate-600">
                    {row[cellIndex] ?? ""}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-6 flex justify-end">
        <button
          type="button"
          onClick={onImport}
          disabled={!canImport || isImporting}
          className="rounded-md bg-teal-800 px-4 py-2 text-sm font-medium text-white hover:bg-teal-900 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isImporting ? "Importing…" : "Import Feedback"}
        </button>
      </div>
    </div>
  );
}

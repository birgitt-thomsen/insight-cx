import { useRef, useState } from "react";
import { UploadCloud } from "lucide-react";
import { REQUIRED_CSV_COLUMNS } from "../../lib/csv";

export function UploadDropzone({
  onFileSelected,
  error,
}: {
  onFileSelected: (file: File) => void;
  error?: string | null;
}) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  function handleFiles(files: FileList | null) {
    const file = files?.[0];
    if (file) onFileSelected(file);
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[2fr_1fr]">
      <div>
        <h2 className="text-lg font-semibold text-slate-900">Upload a CSV file</h2>
        <p className="mt-1 text-sm text-slate-500">
          Drag your export here, or browse your files. Nothing is imported until you confirm.
        </p>

        <div
          role="button"
          tabIndex={0}
          onClick={() => inputRef.current?.click()}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              inputRef.current?.click();
            }
          }}
          onDragOver={(event) => {
            event.preventDefault();
            setIsDragging(true);
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(event) => {
            event.preventDefault();
            setIsDragging(false);
            handleFiles(event.dataTransfer.files);
          }}
          className={`mt-4 flex cursor-pointer flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed p-12 text-center transition-colors ${
            isDragging
              ? "border-indigo-400 bg-indigo-50"
              : "border-slate-300 bg-slate-50 hover:bg-slate-100"
          }`}
        >
          <UploadCloud className="h-8 w-8 text-teal-600" aria-hidden="true" />
          <p className="text-sm font-semibold text-slate-700">Drag and drop your CSV file here</p>
          <p className="text-sm text-slate-500">or choose a file from your computer</p>
          <span className="mt-2 rounded-md border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium text-slate-700 shadow-sm">
            Browse files
          </span>
          <input
            ref={inputRef}
            type="file"
            accept=".csv"
            className="hidden"
            onChange={(event) => handleFiles(event.target.files)}
          />
        </div>

        {error && (
          <p role="alert" className="mt-3 text-sm font-medium text-rose-600">
            {error}
          </p>
        )}
      </div>

      <div className="rounded-xl border border-slate-200 bg-white p-5">
        <h3 className="text-sm font-semibold text-slate-900">File requirements</h3>
        <ul className="mt-3 space-y-1.5 text-sm text-slate-600">
          <li>CSV format (.csv)</li>
          <li>UTF-8 encoding</li>
          <li>Maximum 5,000 feedback records</li>
        </ul>
        <p className="mt-4 text-xs font-semibold uppercase tracking-wide text-slate-400">
          Required columns
        </p>
        <div className="mt-2 flex flex-wrap gap-1.5">
          {REQUIRED_CSV_COLUMNS.map((col) => (
            <span
              key={col}
              className="rounded-full bg-slate-100 px-2 py-0.5 font-mono text-xs text-slate-600"
            >
              {col}
            </span>
          ))}
        </div>
        <p className="mt-4 text-xs text-slate-500">
          Additional columns are allowed and are ignored. Dates must be formatted as{" "}
          <span className="font-mono">YYYY-MM-DD HH:MM:SS</span>.
        </p>
      </div>
    </div>
  );
}

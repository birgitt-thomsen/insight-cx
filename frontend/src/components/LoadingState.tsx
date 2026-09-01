export function LoadingState({ label = "Loading…" }: { label?: string }) {
  return (
    <div
      role="status"
      aria-live="polite"
      className="flex flex-col items-center justify-center gap-3 px-6 py-12 text-center text-sm text-slate-500"
    >
      <span
        aria-hidden="true"
        className="h-6 w-6 animate-spin rounded-full border-2 border-slate-300 border-t-indigo-600"
      />
      <span>{label}</span>
    </div>
  );
}

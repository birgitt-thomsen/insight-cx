export function ErrorState({
  title = "Something went wrong",
  description,
  onRetry,
}: {
  title?: string;
  description?: string;
  onRetry?: () => void;
}) {
  return (
    <div
      role="alert"
      className="flex flex-col items-center justify-center gap-2 rounded-lg border border-rose-200 bg-rose-50 px-6 py-10 text-center"
    >
      <p className="text-sm font-semibold text-rose-700">{title}</p>
      {description && <p className="max-w-md text-sm text-rose-600">{description}</p>}
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-3 rounded-md bg-white px-3 py-1.5 text-sm font-medium text-rose-700 ring-1 ring-inset ring-rose-300 hover:bg-rose-100"
        >
          Try again
        </button>
      )}
    </div>
  );
}

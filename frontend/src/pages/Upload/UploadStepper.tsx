const STEPS = ["Select", "Preview", "Import", "Confirmation"];

export function UploadStepper({ currentIndex }: { currentIndex: number }) {
  return (
    <ol className="flex flex-wrap items-center gap-2 text-sm">
      {STEPS.map((label, index) => {
        const state = index < currentIndex ? "done" : index === currentIndex ? "current" : "upcoming";

        return (
          <li key={label} className="flex items-center gap-2">
            <span
              className={`flex h-6 w-6 items-center justify-center rounded-full text-xs font-semibold ${
                state === "current"
                  ? "bg-teal-800 text-white"
                  : state === "done"
                    ? "bg-teal-100 text-teal-800"
                    : "bg-slate-100 text-slate-400"
              }`}
            >
              {index + 1}
            </span>
            <span className={state === "upcoming" ? "text-slate-400" : "font-medium text-slate-700"}>
              {label}
            </span>
            {index < STEPS.length - 1 && (
              <span className="mx-1 h-px w-6 bg-slate-200" aria-hidden="true" />
            )}
          </li>
        );
      })}
    </ol>
  );
}

import type { ReactNode } from "react";

/**
 * Wraps a form control in its own <label> so it's accessibly associated
 * without needing to wire up matching htmlFor/id pairs at every call site.
 */
export function Field({ label, hint, children }: { label: string; hint?: string; children: ReactNode }) {
  return (
    <label className="flex flex-col gap-1">
      <span className="text-xs font-medium text-slate-500">{label}</span>
      {children}
      {hint && <span className="text-xs text-slate-400">{hint}</span>}
    </label>
  );
}

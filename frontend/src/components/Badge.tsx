import type { ReactNode } from "react";
import {
  confidenceBadgeClasses,
  healthBadgeClasses,
  priorityBadgeClasses,
  sentimentBadgeClasses,
} from "../lib/badgeColors";

export function Badge({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <span
      className={`inline-flex items-center gap-1 whitespace-nowrap rounded-full px-2.5 py-0.5 text-xs font-medium ring-1 ring-inset ${
        className ?? "bg-slate-100 text-slate-600 ring-slate-500/20"
      }`}
    >
      {children}
    </span>
  );
}

export function SentimentBadge({ sentiment }: { sentiment?: string | null }) {
  return <Badge className={sentimentBadgeClasses(sentiment)}>{sentiment ?? "Unknown"}</Badge>;
}

export function PriorityBadge({ priority }: { priority?: string | null }) {
  return (
    <Badge className={priorityBadgeClasses(priority)}>
      {priority ? `${priority} priority` : "Unknown"}
    </Badge>
  );
}

export function HealthBadge({ status, color }: { status: string; color?: string | null }) {
  return <Badge className={healthBadgeClasses(color)}>{status}</Badge>;
}

export function ConfidenceBadge({ level }: { level?: string | null }) {
  return <Badge className={confidenceBadgeClasses(level)}>{level ?? "Unknown"} confidence</Badge>;
}

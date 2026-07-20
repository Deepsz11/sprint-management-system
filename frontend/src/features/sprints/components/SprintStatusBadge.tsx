import { cn } from "@/lib/utils";

import type { SprintStatus } from "../types";

interface SprintStatusBadgeProps {
  readonly status: SprintStatus;
}

const STYLES: Record<SprintStatus, string> = {
  planned:
    "border border-blue-500/40 bg-blue-500/10 text-blue-700 dark:text-blue-300",
  active:
    "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300",
  completed:
    "border border-violet-500/40 bg-violet-500/10 text-violet-700 dark:text-violet-300",
  cancelled: "border border-border bg-muted text-muted-foreground",
};

const LABELS: Record<SprintStatus, string> = {
  planned: "Planned",
  active: "Active",
  completed: "Completed",
  cancelled: "Cancelled",
};

export function SprintStatusBadge({ status }: SprintStatusBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        STYLES[status],
      )}
    >
      {LABELS[status]}
    </span>
  );
}
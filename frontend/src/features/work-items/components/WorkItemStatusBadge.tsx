import { cn } from "@/lib/utils";

import type { WorkItemPriority, WorkItemStatus } from "../types";

const STATUS_STYLES: Record<WorkItemStatus, string> = {
  backlog: "border border-border bg-muted text-muted-foreground",
  todo:
    "border border-slate-500/40 bg-slate-500/10 text-slate-700 dark:text-slate-300",
  in_progress:
    "border border-blue-500/40 bg-blue-500/10 text-blue-700 dark:text-blue-300",
  in_review:
    "border border-amber-500/40 bg-amber-500/10 text-amber-700 dark:text-amber-300",
  done:
    "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300",
  cancelled: "border border-border bg-muted text-muted-foreground line-through",
};

const STATUS_LABELS: Record<WorkItemStatus, string> = {
  backlog: "Backlog",
  todo: "Todo",
  in_progress: "In Progress",
  in_review: "In Review",
  done: "Done",
  cancelled: "Cancelled",
};

const PRIORITY_STYLES: Record<WorkItemPriority, string> = {
  critical:
    "border border-destructive/40 bg-destructive/10 text-destructive",
  high:
    "border border-orange-500/40 bg-orange-500/10 text-orange-700 dark:text-orange-300",
  medium:
    "border border-blue-500/40 bg-blue-500/10 text-blue-700 dark:text-blue-300",
  low: "border border-border bg-muted text-muted-foreground",
};

const PRIORITY_LABELS: Record<WorkItemPriority, string> = {
  critical: "Critical",
  high: "High",
  medium: "Medium",
  low: "Low",
};

export function WorkItemStatusBadge({ status }: { readonly status: WorkItemStatus }) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        STATUS_STYLES[status],
      )}
    >
      {STATUS_LABELS[status]}
    </span>
  );
}

export function WorkItemPriorityBadge({
  priority,
}: {
  readonly priority: WorkItemPriority;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        PRIORITY_STYLES[priority],
      )}
    >
      {PRIORITY_LABELS[priority]}
    </span>
  );
}

export { STATUS_LABELS, PRIORITY_LABELS };
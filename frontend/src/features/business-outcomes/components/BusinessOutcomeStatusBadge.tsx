import { cn } from "@/lib/utils";

import type { OutcomeStatus } from "../types";

const STYLES: Record<OutcomeStatus, string> = {
  proposed: "border border-border bg-muted text-muted-foreground",
  active:
    "border border-blue-500/40 bg-blue-500/10 text-blue-700 dark:text-blue-300",
  achieved:
    "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300",
  at_risk:
    "border border-amber-500/40 bg-amber-500/10 text-amber-700 dark:text-amber-300",
  off_track:
    "border border-destructive/40 bg-destructive/10 text-destructive",
  abandoned:
    "border border-border bg-muted text-muted-foreground line-through",
};

const LABELS: Record<OutcomeStatus, string> = {
  proposed: "Proposed",
  active: "Active",
  achieved: "Achieved",
  at_risk: "At Risk",
  off_track: "Off Track",
  abandoned: "Abandoned",
};

interface BusinessOutcomeStatusBadgeProps {
  readonly status: OutcomeStatus;
}

export function BusinessOutcomeStatusBadge({
  status,
}: BusinessOutcomeStatusBadgeProps) {
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

export { LABELS as OUTCOME_STATUS_LABELS };
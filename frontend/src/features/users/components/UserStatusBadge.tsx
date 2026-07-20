import { cn } from "@/lib/utils";

import type { UserStatus } from "../types";

const STYLES: Record<UserStatus, string> = {
  active:
    "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300",
  invited:
    "border border-blue-500/40 bg-blue-500/10 text-blue-700 dark:text-blue-300",
  suspended:
    "border border-amber-500/40 bg-amber-500/10 text-amber-700 dark:text-amber-300",
  deactivated:
    "border border-border bg-muted text-muted-foreground line-through",
};

const LABELS: Record<UserStatus, string> = {
  active: "Active",
  invited: "Invited",
  suspended: "Suspended",
  deactivated: "Disabled",
};

interface UserStatusBadgeProps {
  readonly status: UserStatus;
}

export function UserStatusBadge({ status }: UserStatusBadgeProps) {
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

export { LABELS as USER_STATUS_LABELS };
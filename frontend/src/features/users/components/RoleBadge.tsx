import { cn } from "@/lib/utils";

import type { UserRole } from "../types";
import { ROLE_LABELS } from "../useRoleOptions";

const STYLES: Record<UserRole, string> = {
  super_admin:
    "border border-violet-500/40 bg-violet-500/10 text-violet-700 dark:text-violet-300",
  org_admin:
    "border border-primary/40 bg-primary/10 text-primary",
  executive:
    "border border-amber-500/40 bg-amber-500/10 text-amber-700 dark:text-amber-300",
  product_manager:
    "border border-blue-500/40 bg-blue-500/10 text-blue-700 dark:text-blue-300",
  engineering_manager:
    "border border-blue-500/40 bg-blue-500/10 text-blue-700 dark:text-blue-300",
  engineer:
    "border border-slate-500/40 bg-slate-500/10 text-slate-700 dark:text-slate-300",
  viewer: "border border-border bg-muted text-muted-foreground",
};

interface RoleBadgeProps {
  readonly role: UserRole;
}

export function RoleBadge({ role }: RoleBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        STYLES[role],
      )}
    >
      {ROLE_LABELS[role]}
    </span>
  );
}
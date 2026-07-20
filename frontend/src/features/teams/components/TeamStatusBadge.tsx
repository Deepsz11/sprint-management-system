import { cn } from "@/lib/utils";

interface TeamStatusBadgeProps {
  readonly isActive: boolean;
}

export function TeamStatusBadge({ isActive }: TeamStatusBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        isActive
          ? "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300"
          : "border border-border bg-muted text-muted-foreground",
      )}
    >
      {isActive ? "Active" : "Inactive"}
    </span>
  );
}
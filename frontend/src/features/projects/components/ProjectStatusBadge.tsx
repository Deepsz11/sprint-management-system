import { cn } from "@/lib/utils";

interface ProjectStatusBadgeProps {
  readonly isArchived: boolean;
}

export function ProjectStatusBadge({ isArchived }: ProjectStatusBadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        isArchived
          ? "border border-border bg-muted text-muted-foreground"
          : "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300",
      )}
    >
      {isArchived ? "Archived" : "Active"}
    </span>
  );
}
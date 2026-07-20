import { Flag, Pencil, PlayCircle, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type { Sprint } from "../types";
import { SprintStatusBadge } from "./SprintStatusBadge";

interface SprintsTableProps {
  readonly sprints: Sprint[];
  readonly onEdit: (sprint: Sprint) => void;
  readonly onDelete: (sprint: Sprint) => void;
  readonly onStart: (sprint: Sprint) => void;
  readonly onComplete: (sprint: Sprint) => void;
  readonly isMutating: boolean;
}

function formatDate(value: string | null): string {
  if (!value) return "—";
  const parsed = Date.parse(value);
  if (Number.isNaN(parsed)) return value;
  return new Date(parsed).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "2-digit",
  });
}

function percent(sprint: Sprint): string {
  if (sprint.planned_capacity <= 0) return "—";
  const value = (sprint.completed_points / sprint.planned_capacity) * 100;
  return `${Math.min(999, Math.max(0, Math.round(value)))}%`;
}

export function SprintsTable({
  sprints,
  onEdit,
  onDelete,
  onStart,
  onComplete,
  isMutating,
}: SprintsTableProps) {
  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Name
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Status
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Window
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Capacity
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Completion
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {sprints.map((sprint) => {
              const canStart = sprint.status === "planned";
              const canComplete = sprint.status === "active";
              const canEdit =
                sprint.status !== "completed" && sprint.status !== "cancelled";
              const canDelete = sprint.status !== "completed";

              return (
                <tr
                  key={sprint.id}
                  className={cn(
                    "transition-colors hover:bg-muted/30",
                    sprint.status === "cancelled" && "opacity-70",
                  )}
                >
                  <td className="px-4 py-3">
                    <div className="flex flex-col">
                      <span className="font-medium text-foreground">
                        {sprint.name}
                      </span>
                      {sprint.goal && (
                        <span className="line-clamp-1 text-xs text-muted-foreground">
                          {sprint.goal}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <SprintStatusBadge status={sprint.status} />
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    <div className="flex flex-col">
                      <span>{formatDate(sprint.start_date)}</span>
                      <span className="text-xs opacity-80">
                        → {formatDate(sprint.end_date)}
                      </span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-foreground">
                    {sprint.planned_capacity}
                  </td>
                  <td className="px-4 py-3 text-foreground">
                    <div className="flex flex-col">
                      <span>
                        {sprint.completed_points} / {sprint.planned_capacity}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        {percent(sprint)}
                      </span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center justify-end gap-1">
                      {canStart && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          aria-label={`Start ${sprint.name}`}
                          onClick={() => onStart(sprint)}
                          disabled={isMutating}
                          title="Start sprint"
                        >
                          <PlayCircle className="h-4 w-4" />
                        </Button>
                      )}
                      {canComplete && (
                        <Button
                          type="button"
                          variant="ghost"
                          size="icon"
                          aria-label={`Complete ${sprint.name}`}
                          onClick={() => onComplete(sprint)}
                          disabled={isMutating}
                          title="Complete sprint"
                        >
                          <Flag className="h-4 w-4" />
                        </Button>
                      )}
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Edit ${sprint.name}`}
                        onClick={() => onEdit(sprint)}
                        disabled={isMutating || !canEdit}
                        title="Edit sprint"
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Delete ${sprint.name}`}
                        onClick={() => onDelete(sprint)}
                        disabled={isMutating || !canDelete}
                        title={
                          canDelete
                            ? "Delete sprint"
                            : "Completed sprints cannot be deleted"
                        }
                        className="text-destructive hover:bg-destructive/10 hover:text-destructive disabled:text-muted-foreground"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
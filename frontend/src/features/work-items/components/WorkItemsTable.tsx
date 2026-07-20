import { Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type {
  WorkItem,
  WorkItemAssigneeOption,
  WorkItemSprintOption,
} from "../types";
import {
  WorkItemPriorityBadge,
  WorkItemStatusBadge,
} from "./WorkItemStatusBadge";

interface WorkItemsTableProps {
  readonly items: WorkItem[];
  readonly sprints: WorkItemSprintOption[];
  readonly assignees: WorkItemAssigneeOption[];
  readonly isMutating: boolean;
  readonly onEdit: (item: WorkItem) => void;
  readonly onDelete: (item: WorkItem) => void;
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

export function WorkItemsTable({
  items,
  sprints,
  assignees,
  isMutating,
  onEdit,
  onDelete,
}: WorkItemsTableProps) {
  const sprintMap = new Map(sprints.map((sprint) => [sprint.id, sprint.name]));
  const assigneeMap = new Map(
    assignees.map((user) => [user.id, user.full_name]),
  );

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Title
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Sprint
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Assignee
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Priority
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Status
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Points
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Completed
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {items.map((item) => {
              const canEdit = item.status !== "cancelled";
              const canDelete = item.status !== "done";
              return (
                <tr
                  key={item.id}
                  className={cn(
                    "transition-colors hover:bg-muted/30",
                    item.status === "cancelled" && "opacity-70",
                  )}
                >
                  <td className="px-4 py-3">
                    <div className="flex flex-col">
                      <span className="font-medium text-foreground">
                        {item.title}
                      </span>
                      {item.description && (
                        <span className="line-clamp-1 text-xs text-muted-foreground">
                          {item.description}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {item.sprint_id
                      ? sprintMap.get(item.sprint_id) ?? "—"
                      : "Backlog"}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {item.assignee_id
                      ? assigneeMap.get(item.assignee_id) ?? "—"
                      : "Unassigned"}
                  </td>
                  <td className="px-4 py-3">
                    <WorkItemPriorityBadge priority={item.priority} />
                  </td>
                  <td className="px-4 py-3">
                    <WorkItemStatusBadge status={item.status} />
                  </td>
                  <td className="px-4 py-3 text-foreground">
                    {item.story_points ?? "—"}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {formatDate(item.completed_at)}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center justify-end gap-1">
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Edit ${item.title}`}
                        onClick={() => onEdit(item)}
                        disabled={isMutating || !canEdit}
                        title={
                          canEdit
                            ? "Edit work item"
                            : "Cancelled items cannot be edited"
                        }
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Delete ${item.title}`}
                        onClick={() => onDelete(item)}
                        disabled={isMutating || !canDelete}
                        title={
                          canDelete
                            ? "Delete work item"
                            : "Completed items cannot be deleted"
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
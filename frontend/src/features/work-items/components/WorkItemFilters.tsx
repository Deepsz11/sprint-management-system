import { Search } from "lucide-react";

import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { Button } from "@/components/ui/Button";

import type {
  WorkItemAssigneeOption,
  WorkItemPriority,
  WorkItemProjectOption,
  WorkItemSprintOption,
  WorkItemStatus,
  WorkItemType,
} from "../types";
import {
  ITEM_TYPE_OPTIONS,
  PRIORITY_OPTIONS,
  STATUS_OPTIONS,
} from "../workItemSchemas";

interface WorkItemFiltersProps {
  readonly projects: WorkItemProjectOption[];
  readonly sprints: WorkItemSprintOption[];
  readonly assignees: WorkItemAssigneeOption[];
  readonly isLoadingProjects: boolean;
  readonly isLoadingSprints: boolean;
  readonly isLoadingAssignees: boolean;
  readonly projectId: string | null;
  readonly sprintId: string | null;
  readonly assigneeId: string | null;
  readonly itemTypes: readonly WorkItemType[];
  readonly statuses: readonly WorkItemStatus[];
  readonly priorities: readonly WorkItemPriority[];
  readonly search: string;
  readonly onProjectChange: (value: string | null) => void;
  readonly onSprintChange: (value: string | null) => void;
  readonly onAssigneeChange: (value: string | null) => void;
  readonly onItemTypeChange: (value: WorkItemType | "") => void;
  readonly onStatusChange: (value: WorkItemStatus | "") => void;
  readonly onPriorityChange: (value: WorkItemPriority | "") => void;
  readonly onSearchChange: (value: string) => void;
  readonly onReset: () => void;
}

const LABELS_ITEM_TYPE: Record<WorkItemType, string> = {
  epic: "Epic",
  story: "Story",
  task: "Task",
  bug: "Bug",
  spike: "Spike",
};

const LABELS_STATUS: Record<WorkItemStatus, string> = {
  backlog: "Backlog",
  todo: "Todo",
  in_progress: "In Progress",
  in_review: "In Review",
  done: "Done",
  cancelled: "Cancelled",
};

const LABELS_PRIORITY: Record<WorkItemPriority, string> = {
  critical: "Critical",
  high: "High",
  medium: "Medium",
  low: "Low",
};

export function WorkItemFilters({
  projects,
  sprints,
  assignees,
  isLoadingProjects,
  isLoadingSprints,
  isLoadingAssignees,
  projectId,
  sprintId,
  assigneeId,
  itemTypes,
  statuses,
  priorities,
  search,
  onProjectChange,
  onSprintChange,
  onAssigneeChange,
  onItemTypeChange,
  onStatusChange,
  onPriorityChange,
  onSearchChange,
  onReset,
}: WorkItemFiltersProps) {
  const activeType = itemTypes[0] ?? "";
  const activeStatus = statuses[0] ?? "";
  const activePriority = priorities[0] ?? "";

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card p-4">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div className="space-y-2">
          <Label htmlFor="wi-project">Project</Label>
          <select
            id="wi-project"
            value={projectId ?? ""}
            onChange={(event) =>
              onProjectChange(event.target.value ? event.target.value : null)
            }
            disabled={isLoadingProjects}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">
              {isLoadingProjects ? "Loading…" : "All projects"}
            </option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name} ({project.key})
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="wi-sprint">Sprint</Label>
          <select
            id="wi-sprint"
            value={sprintId ?? ""}
            onChange={(event) =>
              onSprintChange(event.target.value ? event.target.value : null)
            }
            disabled={!projectId || isLoadingSprints}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">
              {!projectId
                ? "Select a project first"
                : isLoadingSprints
                ? "Loading…"
                : "All sprints"}
            </option>
            {sprints.map((sprint) => (
              <option key={sprint.id} value={sprint.id}>
                {sprint.name}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="wi-assignee">Assignee</Label>
          <select
            id="wi-assignee"
            value={assigneeId ?? ""}
            onChange={(event) =>
              onAssigneeChange(event.target.value ? event.target.value : null)
            }
            disabled={isLoadingAssignees}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">
              {isLoadingAssignees ? "Loading…" : "All assignees"}
            </option>
            {assignees.map((user) => (
              <option key={user.id} value={user.id}>
                {user.full_name}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="wi-type">Type</Label>
          <select
            id="wi-type"
            value={activeType}
            onChange={(event) =>
              onItemTypeChange(event.target.value as WorkItemType | "")
            }
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">All types</option>
            {ITEM_TYPE_OPTIONS.map((value) => (
              <option key={value} value={value}>
                {LABELS_ITEM_TYPE[value]}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="wi-status">Status</Label>
          <select
            id="wi-status"
            value={activeStatus}
            onChange={(event) =>
              onStatusChange(event.target.value as WorkItemStatus | "")
            }
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">All statuses</option>
            {STATUS_OPTIONS.map((value) => (
              <option key={value} value={value}>
                {LABELS_STATUS[value]}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="wi-priority">Priority</Label>
          <select
            id="wi-priority"
            value={activePriority}
            onChange={(event) =>
              onPriorityChange(event.target.value as WorkItemPriority | "")
            }
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">All priorities</option>
            {PRIORITY_OPTIONS.map((value) => (
              <option key={value} value={value}>
                {LABELS_PRIORITY[value]}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative w-full sm:max-w-md">
          <Search
            aria-hidden="true"
            className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
          />
          <Input
            type="search"
            placeholder="Search by title…"
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            className="pl-9"
            aria-label="Search work items"
          />
        </div>
        <Button type="button" variant="outline" onClick={onReset}>
          Reset filters
        </Button>
      </div>
    </div>
  );
}
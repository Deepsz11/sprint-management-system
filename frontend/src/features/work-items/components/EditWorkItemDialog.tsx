import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import { useAssigneeOptions } from "../useAssigneeOptions";
import { useSprintOptions } from "../useSprintOptions";
import type {
  UpdateWorkItemInput,
  WorkItem,
  WorkItemPriority,
  WorkItemStatus,
} from "../types";
import {
  PRIORITY_OPTIONS,
  STATUS_OPTIONS,
  editWorkItemSchema,
  parseLabels,
  stringifyLabels,
  type EditWorkItemFormValues,
} from "../workItemSchemas";
import { Modal } from "./Modal";

interface EditWorkItemDialogProps {
  readonly open: boolean;
  readonly workItem: WorkItem | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: UpdateWorkItemInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

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

export function EditWorkItemDialog({
  open,
  workItem,
  onClose,
  onSubmit,
  isSubmitting,
}: EditWorkItemDialogProps) {
  const { toast } = useToast();

  const projectId = workItem?.project_id ?? null;
  const { sprints, isLoadingSprints } = useSprintOptions(projectId);
  const { assignees, isLoading: isLoadingAssignees } = useAssigneeOptions();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditWorkItemFormValues>({
    resolver: zodResolver(editWorkItemSchema),
    defaultValues: {
      title: "",
      description: "",
      status: "backlog",
      priority: "medium",
      story_points: "",
      estimated_hours: "",
      sprint_id: "",
      assignee_id: "",
      labels: "",
    },
  });

  useEffect(() => {
    if (open && workItem) {
      reset({
        title: workItem.title,
        description: workItem.description ?? "",
        status: workItem.status,
        priority: workItem.priority,
        story_points: workItem.story_points ?? "",
        estimated_hours: workItem.estimated_hours ?? "",
        sprint_id: workItem.sprint_id ?? "",
        assignee_id: workItem.assignee_id ?? "",
        labels: stringifyLabels(workItem.labels),
      });
    }
  }, [open, workItem, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!workItem) return;
    try {
      const input: UpdateWorkItemInput = {
        title: values.title.trim(),
        description: values.description ? values.description.trim() : null,
        status: values.status,
        priority: values.priority,
        story_points:
          typeof values.story_points === "number" ? values.story_points : null,
        estimated_hours:
          typeof values.estimated_hours === "number"
            ? values.estimated_hours
            : null,
        sprint_id: values.sprint_id ? values.sprint_id : null,
        assignee_id: values.assignee_id ? values.assignee_id : null,
        labels: parseLabels(values.labels ?? ""),
      };
      await onSubmit(workItem.id, input);
      toast({ title: "Work item updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update work item",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && workItem !== null}
      onClose={onClose}
      title={`Edit ${workItem?.title ?? "work item"}`}
      description={workItem ? `Type: ${workItem.item_type}` : undefined}
      maxWidthClassName="max-w-2xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="edit-wi-title">Title</Label>
          <Input
            id="edit-wi-title"
            {...register("title")}
            aria-invalid={Boolean(errors.title)}
          />
          {errors.title && (
            <p className="text-xs text-destructive">{errors.title.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="edit-wi-description">Description</Label>
          <textarea
            id="edit-wi-description"
            rows={3}
            {...register("description")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="edit-wi-status">Status</Label>
            <select
              id="edit-wi-status"
              {...register("status")}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {STATUS_OPTIONS.map((value) => (
                <option key={value} value={value}>
                  {LABELS_STATUS[value]}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-wi-priority">Priority</Label>
            <select
              id="edit-wi-priority"
              {...register("priority")}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {PRIORITY_OPTIONS.map((value) => (
                <option key={value} value={value}>
                  {LABELS_PRIORITY[value]}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="edit-wi-points">Story points</Label>
            <Input
              id="edit-wi-points"
              type="number"
              min={0}
              step={1}
              {...register("story_points")}
              aria-invalid={Boolean(errors.story_points)}
            />
            {errors.story_points && (
              <p className="text-xs text-destructive">
                {errors.story_points.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-wi-estimate">Estimate (hours)</Label>
            <Input
              id="edit-wi-estimate"
              type="number"
              min={0}
              step={0.5}
              {...register("estimated_hours")}
              aria-invalid={Boolean(errors.estimated_hours)}
            />
            {errors.estimated_hours && (
              <p className="text-xs text-destructive">
                {errors.estimated_hours.message}
              </p>
            )}
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="edit-wi-sprint">Sprint</Label>
            <select
              id="edit-wi-sprint"
              {...register("sprint_id")}
              disabled={!projectId || isLoadingSprints}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <option value="">
                {isLoadingSprints ? "Loading…" : "Backlog (no sprint)"}
              </option>
              {sprints.map((sprint) => (
                <option key={sprint.id} value={sprint.id}>
                  {sprint.name}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="edit-wi-assignee">Assignee</Label>
            <select
              id="edit-wi-assignee"
              {...register("assignee_id")}
              disabled={isLoadingAssignees}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <option value="">
                {isLoadingAssignees ? "Loading…" : "Unassigned"}
              </option>
              {assignees.map((user) => (
                <option key={user.id} value={user.id}>
                  {user.full_name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="edit-wi-labels">Labels</Label>
          <Input
            id="edit-wi-labels"
            placeholder="comma,separated,labels"
            {...register("labels")}
          />
        </div>

        <div className="flex items-center justify-end gap-2 pt-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={submitting}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={submitting || !isDirty}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Saving…
              </>
            ) : (
              "Save changes"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
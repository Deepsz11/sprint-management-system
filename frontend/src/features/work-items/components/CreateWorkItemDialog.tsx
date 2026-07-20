import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import { useAssigneeOptions } from "../useAssigneeOptions";
import { useSprintOptions } from "../useSprintOptions";
import type {
  CreateWorkItemInput,
  WorkItemPriority,
  WorkItemType,
} from "../types";
import {
  ITEM_TYPE_OPTIONS,
  PRIORITY_OPTIONS,
  createWorkItemSchema,
  parseLabels,
  type CreateWorkItemFormValues,
} from "../workItemSchemas";
import { Modal } from "./Modal";

interface CreateWorkItemDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: CreateWorkItemInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly defaultProjectId: string | null;
}

const LABELS_ITEM_TYPE: Record<WorkItemType, string> = {
  epic: "Epic",
  story: "Story",
  task: "Task",
  bug: "Bug",
  spike: "Spike",
};

const LABELS_PRIORITY: Record<WorkItemPriority, string> = {
  critical: "Critical",
  high: "High",
  medium: "Medium",
  low: "Low",
};

export function CreateWorkItemDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
  defaultProjectId,
}: CreateWorkItemDialogProps) {
  const { toast } = useToast();
  const [selectedProject, setSelectedProject] = useState<string | null>(
    defaultProjectId,
  );

  const {
    projects,
    sprints,
    isLoadingProjects,
    isLoadingSprints,
  } = useSprintOptions(selectedProject);
  const { assignees, isLoading: isLoadingAssignees } = useAssigneeOptions();

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CreateWorkItemFormValues>({
    resolver: zodResolver(createWorkItemSchema),
    defaultValues: {
      project_id: defaultProjectId ?? "",
      sprint_id: "",
      title: "",
      description: "",
      item_type: "story",
      priority: "medium",
      story_points: "",
      estimated_hours: "",
      assignee_id: "",
      labels: "",
    },
  });

  useEffect(() => {
    if (open) {
      setSelectedProject(defaultProjectId);
      reset({
        project_id: defaultProjectId ?? "",
        sprint_id: "",
        title: "",
        description: "",
        item_type: "story",
        priority: "medium",
        story_points: "",
        estimated_hours: "",
        assignee_id: "",
        labels: "",
      });
    }
  }, [open, defaultProjectId, reset]);

  const watchedProject = watch("project_id");

  useEffect(() => {
    if (watchedProject !== selectedProject) {
      setSelectedProject(watchedProject ? watchedProject : null);
      setValue("sprint_id", "");
    }
  }, [watchedProject, selectedProject, setValue]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    try {
      const input: CreateWorkItemInput = {
        project_id: values.project_id,
        sprint_id: values.sprint_id ? values.sprint_id : null,
        title: values.title.trim(),
        description: values.description ? values.description.trim() : null,
        item_type: values.item_type,
        priority: values.priority,
        story_points:
          typeof values.story_points === "number" ? values.story_points : null,
        estimated_hours:
          typeof values.estimated_hours === "number"
            ? values.estimated_hours
            : null,
        assignee_id: values.assignee_id ? values.assignee_id : null,
        labels: parseLabels(values.labels ?? ""),
      };
      await onSubmit(input);
      toast({ title: "Work item created", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not create work item",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Create work item"
      description="Add a story, task, bug, spike, or epic to a project."
      maxWidthClassName="max-w-2xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="create-wi-project">Project</Label>
            <select
              id="create-wi-project"
              {...register("project_id")}
              disabled={isLoadingProjects}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
              aria-invalid={Boolean(errors.project_id)}
            >
              <option value="">
                {isLoadingProjects ? "Loading projects…" : "Select a project"}
              </option>
              {projects.map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name} ({project.key})
                </option>
              ))}
            </select>
            {errors.project_id && (
              <p className="text-xs text-destructive">
                {errors.project_id.message}
              </p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="create-wi-sprint">Sprint</Label>
            <select
              id="create-wi-sprint"
              {...register("sprint_id")}
              disabled={!selectedProject || isLoadingSprints}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <option value="">
                {!selectedProject
                  ? "Select a project first"
                  : isLoadingSprints
                  ? "Loading…"
                  : "Backlog (no sprint)"}
              </option>
              {sprints.map((sprint) => (
                <option key={sprint.id} value={sprint.id}>
                  {sprint.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="create-wi-title">Title</Label>
          <Input
            id="create-wi-title"
            placeholder="e.g. Improve onboarding conversion"
            {...register("title")}
            aria-invalid={Boolean(errors.title)}
          />
          {errors.title && (
            <p className="text-xs text-destructive">{errors.title.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="create-wi-description">Description</Label>
          <textarea
            id="create-wi-description"
            rows={3}
            {...register("description")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="Describe the outcome, context, and acceptance criteria"
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="create-wi-type">Type</Label>
            <select
              id="create-wi-type"
              {...register("item_type")}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {ITEM_TYPE_OPTIONS.map((value) => (
                <option key={value} value={value}>
                  {LABELS_ITEM_TYPE[value]}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="create-wi-priority">Priority</Label>
            <select
              id="create-wi-priority"
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
            <Label htmlFor="create-wi-points">Story points</Label>
            <Input
              id="create-wi-points"
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
            <Label htmlFor="create-wi-estimate">Estimate (hours)</Label>
            <Input
              id="create-wi-estimate"
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
            <Label htmlFor="create-wi-assignee">Assignee</Label>
            <select
              id="create-wi-assignee"
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
          <div className="space-y-2">
            <Label htmlFor="create-wi-labels">Labels</Label>
            <Input
              id="create-wi-labels"
              placeholder="comma,separated,labels"
              {...register("labels")}
            />
          </div>
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
          <Button type="submit" disabled={submitting}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Creating…
              </>
            ) : (
              "Create work item"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
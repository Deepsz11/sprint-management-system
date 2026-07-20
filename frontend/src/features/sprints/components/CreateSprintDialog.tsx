import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import {
  createSprintSchema,
  type CreateSprintFormValues,
} from "../sprintSchemas";
import type { CreateSprintInput, SprintProjectOption } from "../types";
import { Modal } from "./Modal";

interface CreateSprintDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: CreateSprintInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly projects: SprintProjectOption[];
  readonly projectsLoading: boolean;
  readonly defaultProjectId: string | null;
}

export function CreateSprintDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
  projects,
  projectsLoading,
  defaultProjectId,
}: CreateSprintDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CreateSprintFormValues>({
    resolver: zodResolver(createSprintSchema),
    defaultValues: {
      project_id: defaultProjectId ?? "",
      name: "",
      goal: "",
      start_date: "",
      end_date: "",
      planned_capacity: 0,
    },
  });

  useEffect(() => {
    if (open) {
      reset({
        project_id: defaultProjectId ?? "",
        name: "",
        goal: "",
        start_date: "",
        end_date: "",
        planned_capacity: 0,
      });
    }
  }, [open, defaultProjectId, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    try {
      const input: CreateSprintInput = {
        project_id: values.project_id,
        name: values.name.trim(),
        goal: values.goal ? values.goal.trim() : null,
        start_date: values.start_date,
        end_date: values.end_date,
        planned_capacity: values.planned_capacity,
      };
      await onSubmit(input);
      toast({ title: "Sprint created", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not create sprint",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Create sprint"
      description="Time-box a scope of work and track its outcome."
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="create-project">Project</Label>
          <select
            id="create-project"
            {...register("project_id")}
            disabled={projectsLoading}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            aria-invalid={Boolean(errors.project_id)}
          >
            <option value="">
              {projectsLoading ? "Loading projects…" : "Select a project"}
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
          <Label htmlFor="create-name">Name</Label>
          <Input
            id="create-name"
            placeholder="e.g. Sprint 12 — Onboarding polish"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="create-goal">Goal</Label>
          <textarea
            id="create-goal"
            rows={3}
            {...register("goal")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="What outcome should this sprint deliver?"
          />
          {errors.goal && (
            <p className="text-xs text-destructive">{errors.goal.message}</p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="create-start">Start date</Label>
            <Input
              id="create-start"
              type="date"
              {...register("start_date")}
              aria-invalid={Boolean(errors.start_date)}
            />
            {errors.start_date && (
              <p className="text-xs text-destructive">
                {errors.start_date.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="create-end">End date</Label>
            <Input
              id="create-end"
              type="date"
              {...register("end_date")}
              aria-invalid={Boolean(errors.end_date)}
            />
            {errors.end_date && (
              <p className="text-xs text-destructive">
                {errors.end_date.message}
              </p>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="create-capacity">Planned capacity (points)</Label>
          <Input
            id="create-capacity"
            type="number"
            min={0}
            step={1}
            {...register("planned_capacity")}
            aria-invalid={Boolean(errors.planned_capacity)}
          />
          {errors.planned_capacity && (
            <p className="text-xs text-destructive">
              {errors.planned_capacity.message}
            </p>
          )}
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
              "Create sprint"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
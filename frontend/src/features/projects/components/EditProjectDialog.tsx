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
  editProjectSchema,
  type EditProjectFormValues,
} from "../projectSchemas";
import type { Project, UpdateProjectInput } from "../types";
import { Modal } from "./Modal";

interface EditProjectDialogProps {
  readonly open: boolean;
  readonly project: Project | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: UpdateProjectInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function EditProjectDialog({
  open,
  project,
  onClose,
  onSubmit,
  isSubmitting,
}: EditProjectDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditProjectFormValues>({
    resolver: zodResolver(editProjectSchema),
    defaultValues: {
      name: "",
      description: "",
      start_date: "",
      target_end_date: "",
      is_archived: false,
    },
  });

  useEffect(() => {
    if (open && project) {
      reset({
        name: project.name,
        description: project.description ?? "",
        start_date: project.start_date ?? "",
        target_end_date: project.target_end_date ?? "",
        is_archived: project.is_archived,
      });
    }
  }, [open, project, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!project) return;
    try {
      const input: UpdateProjectInput = {
        name: values.name.trim(),
        description: values.description ? values.description.trim() : null,
        start_date: values.start_date ? values.start_date : null,
        target_end_date: values.target_end_date ? values.target_end_date : null,
        is_archived: values.is_archived,
      };
      await onSubmit(project.id, input);
      toast({ title: "Project updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update project",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && project !== null}
      onClose={onClose}
      title={`Edit ${project?.name ?? "project"}`}
      description={
        project ? `${project.key} • ${project.slug}` : undefined
      }
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="edit-name">Name</Label>
          <Input
            id="edit-name"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="edit-description">Description</Label>
          <textarea
            id="edit-description"
            rows={3}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            {...register("description")}
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="edit-start">Start date</Label>
            <Input
              id="edit-start"
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
            <Label htmlFor="edit-target">Target end date</Label>
            <Input
              id="edit-target"
              type="date"
              {...register("target_end_date")}
              aria-invalid={Boolean(errors.target_end_date)}
            />
            {errors.target_end_date && (
              <p className="text-xs text-destructive">
                {errors.target_end_date.message}
              </p>
            )}
          </div>
        </div>

        <label className="inline-flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            className="h-4 w-4 rounded border-input text-primary focus:ring-2 focus:ring-ring"
            {...register("is_archived")}
          />
          Archived
        </label>

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
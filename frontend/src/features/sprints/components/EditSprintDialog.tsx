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
  editSprintSchema,
  type EditSprintFormValues,
} from "../sprintSchemas";
import type { Sprint, UpdateSprintInput } from "../types";
import { Modal } from "./Modal";

interface EditSprintDialogProps {
  readonly open: boolean;
  readonly sprint: Sprint | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: UpdateSprintInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function EditSprintDialog({
  open,
  sprint,
  onClose,
  onSubmit,
  isSubmitting,
}: EditSprintDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditSprintFormValues>({
    resolver: zodResolver(editSprintSchema),
    defaultValues: {
      name: "",
      goal: "",
      start_date: "",
      end_date: "",
      planned_capacity: 0,
    },
  });

  useEffect(() => {
    if (open && sprint) {
      reset({
        name: sprint.name,
        goal: sprint.goal ?? "",
        start_date: sprint.start_date,
        end_date: sprint.end_date,
        planned_capacity: sprint.planned_capacity,
      });
    }
  }, [open, sprint, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!sprint) return;
    try {
      const input: UpdateSprintInput = {
        name: values.name.trim(),
        goal: values.goal ? values.goal.trim() : null,
        start_date: values.start_date,
        end_date: values.end_date,
        planned_capacity: values.planned_capacity,
      };
      await onSubmit(sprint.id, input);
      toast({ title: "Sprint updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update sprint",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && sprint !== null}
      onClose={onClose}
      title={`Edit ${sprint?.name ?? "sprint"}`}
      description={sprint ? `Status: ${sprint.status}` : undefined}
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
          <Label htmlFor="edit-goal">Goal</Label>
          <textarea
            id="edit-goal"
            rows={3}
            {...register("goal")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          {errors.goal && (
            <p className="text-xs text-destructive">{errors.goal.message}</p>
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
            <Label htmlFor="edit-end">End date</Label>
            <Input
              id="edit-end"
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
          <Label htmlFor="edit-capacity">Planned capacity (points)</Label>
          <Input
            id="edit-capacity"
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
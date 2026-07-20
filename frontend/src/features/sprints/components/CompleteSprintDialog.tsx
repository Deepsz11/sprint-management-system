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
  completeSprintSchema,
  type CompleteSprintFormValues,
} from "../sprintSchemas";
import type { CompleteSprintInput, Sprint } from "../types";
import { Modal } from "./Modal";

interface CompleteSprintDialogProps {
  readonly open: boolean;
  readonly sprint: Sprint | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: CompleteSprintInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function CompleteSprintDialog({
  open,
  sprint,
  onClose,
  onSubmit,
  isSubmitting,
}: CompleteSprintDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CompleteSprintFormValues>({
    resolver: zodResolver(completeSprintSchema),
    defaultValues: { completed_points: 0 },
  });

  useEffect(() => {
    if (open && sprint) {
      reset({ completed_points: sprint.planned_capacity });
    }
  }, [open, sprint, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!sprint) return;
    try {
      await onSubmit(sprint.id, {
        completed_points: values.completed_points,
      });
      toast({ title: "Sprint completed", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not complete sprint",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && sprint !== null}
      onClose={onClose}
      title={`Complete ${sprint?.name ?? "sprint"}`}
      description="Record the final velocity for this sprint."
      maxWidthClassName="max-w-md"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="completed-points">Completed points</Label>
          <Input
            id="completed-points"
            type="number"
            min={0}
            step={1}
            {...register("completed_points")}
            aria-invalid={Boolean(errors.completed_points)}
          />
          {sprint && (
            <p className="text-xs text-muted-foreground">
              Planned capacity: {sprint.planned_capacity}
            </p>
          )}
          {errors.completed_points && (
            <p className="text-xs text-destructive">
              {errors.completed_points.message}
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
                Completing…
              </>
            ) : (
              "Complete sprint"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
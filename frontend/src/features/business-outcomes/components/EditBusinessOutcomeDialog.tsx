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
  OUTCOME_STATUS_OPTIONS,
  editBusinessOutcomeSchema,
  emptyToNull,
  type EditBusinessOutcomeFormValues,
} from "../businessOutcomeSchemas";
import type {
  BusinessOutcome,
  OutcomeOwnerOption,
  UpdateBusinessOutcomeInput,
} from "../types";
import { Modal } from "./Modal";
import { OUTCOME_STATUS_LABELS } from "./BusinessOutcomeStatusBadge";

interface EditBusinessOutcomeDialogProps {
  readonly open: boolean;
  readonly outcome: BusinessOutcome | null;
  readonly owners: OutcomeOwnerOption[];
  readonly ownersLoading: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (
    id: string,
    input: UpdateBusinessOutcomeInput,
  ) => Promise<void>;
  readonly isSubmitting: boolean;
}

function toStringOrEmpty(
  value: string | number | null | undefined,
): string {
  if (value === null || value === undefined) return "";
  return String(value);
}

export function EditBusinessOutcomeDialog({
  open,
  outcome,
  owners,
  ownersLoading,
  onClose,
  onSubmit,
  isSubmitting,
}: EditBusinessOutcomeDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditBusinessOutcomeFormValues>({
    resolver: zodResolver(editBusinessOutcomeSchema),
    defaultValues: {
      name: "",
      description: "",
      hypothesis: "",
      owner_id: "",
      status: "proposed",
      target_date: "",
      baseline_value: "",
      target_value: "",
      current_value: "",
      confidence_score: "",
      financial_impact_estimate: "",
    },
  });

  useEffect(() => {
    if (open && outcome) {
      reset({
        name: outcome.name,
        description: outcome.description ?? "",
        hypothesis: outcome.hypothesis ?? "",
        owner_id: outcome.owner_id ?? "",
        status: outcome.status,
        target_date: outcome.target_date ?? "",
        baseline_value: toStringOrEmpty(outcome.baseline_value),
        target_value: toStringOrEmpty(outcome.target_value),
        current_value: toStringOrEmpty(outcome.current_value),
        confidence_score: toStringOrEmpty(outcome.confidence_score),
        financial_impact_estimate: toStringOrEmpty(
          outcome.financial_impact_estimate,
        ),
      });
    }
  }, [open, outcome, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!outcome) return;
    try {
      const input: UpdateBusinessOutcomeInput = {
        name: values.name.trim(),
        description: emptyToNull(values.description),
        hypothesis: emptyToNull(values.hypothesis),
        owner_id: values.owner_id ? values.owner_id : null,
        status: values.status,
        target_date: emptyToNull(values.target_date),
        baseline_value: emptyToNull(values.baseline_value),
        target_value: emptyToNull(values.target_value),
        current_value: emptyToNull(values.current_value),
        confidence_score: emptyToNull(values.confidence_score),
        financial_impact_estimate: emptyToNull(
          values.financial_impact_estimate,
        ),
      };
      await onSubmit(outcome.id, input);
      toast({ title: "Business outcome updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update outcome",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && outcome !== null}
      onClose={onClose}
      title={`Edit ${outcome?.name ?? "outcome"}`}
      description={outcome ? `Status: ${outcome.status}` : undefined}
      maxWidthClassName="max-w-2xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="bo-edit-name">Name</Label>
          <Input
            id="bo-edit-name"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="bo-edit-description">Description</Label>
          <textarea
            id="bo-edit-description"
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

        <div className="space-y-2">
          <Label htmlFor="bo-edit-hypothesis">Hypothesis</Label>
          <textarea
            id="bo-edit-hypothesis"
            rows={2}
            {...register("hypothesis")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          {errors.hypothesis && (
            <p className="text-xs text-destructive">
              {errors.hypothesis.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <Label htmlFor="bo-edit-status">Status</Label>
            <select
              id="bo-edit-status"
              {...register("status")}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {OUTCOME_STATUS_OPTIONS.map((status) => (
                <option key={status} value={status}>
                  {OUTCOME_STATUS_LABELS[status]}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="bo-edit-owner">Owner</Label>
            <select
              id="bo-edit-owner"
              {...register("owner_id")}
              disabled={ownersLoading}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <option value="">
                {ownersLoading ? "Loading…" : "Unassigned"}
              </option>
              {owners.map((owner) => (
                <option key={owner.id} value={owner.id}>
                  {owner.full_name}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="bo-edit-target-date">Target date</Label>
            <Input
              id="bo-edit-target-date"
              type="date"
              {...register("target_date")}
              aria-invalid={Boolean(errors.target_date)}
            />
            {errors.target_date && (
              <p className="text-xs text-destructive">
                {errors.target_date.message}
              </p>
            )}
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <Label htmlFor="bo-edit-baseline">Baseline value</Label>
            <Input
              id="bo-edit-baseline"
              inputMode="decimal"
              {...register("baseline_value")}
              aria-invalid={Boolean(errors.baseline_value)}
            />
            {errors.baseline_value && (
              <p className="text-xs text-destructive">
                {errors.baseline_value.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="bo-edit-target">Target value</Label>
            <Input
              id="bo-edit-target"
              inputMode="decimal"
              {...register("target_value")}
              aria-invalid={Boolean(errors.target_value)}
            />
            {errors.target_value && (
              <p className="text-xs text-destructive">
                {errors.target_value.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="bo-edit-current">Current value</Label>
            <Input
              id="bo-edit-current"
              inputMode="decimal"
              {...register("current_value")}
              aria-invalid={Boolean(errors.current_value)}
            />
            {errors.current_value && (
              <p className="text-xs text-destructive">
                {errors.current_value.message}
              </p>
            )}
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="bo-edit-confidence">Confidence score (%)</Label>
            <Input
              id="bo-edit-confidence"
              inputMode="decimal"
              {...register("confidence_score")}
              aria-invalid={Boolean(errors.confidence_score)}
            />
            {errors.confidence_score && (
              <p className="text-xs text-destructive">
                {errors.confidence_score.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="bo-edit-impact">Financial impact estimate</Label>
            <Input
              id="bo-edit-impact"
              inputMode="decimal"
              {...register("financial_impact_estimate")}
              aria-invalid={Boolean(errors.financial_impact_estimate)}
            />
            {errors.financial_impact_estimate && (
              <p className="text-xs text-destructive">
                {errors.financial_impact_estimate.message}
              </p>
            )}
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
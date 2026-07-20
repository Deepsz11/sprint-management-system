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
  createBusinessOutcomeSchema,
  emptyToNull,
  type CreateBusinessOutcomeFormValues,
} from "../businessOutcomeSchemas";
import type {
  CreateBusinessOutcomeInput,
  OutcomeOwnerOption,
} from "../types";
import { Modal } from "./Modal";

interface CreateBusinessOutcomeDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: CreateBusinessOutcomeInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly owners: OutcomeOwnerOption[];
  readonly ownersLoading: boolean;
}

export function CreateBusinessOutcomeDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
  owners,
  ownersLoading,
}: CreateBusinessOutcomeDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CreateBusinessOutcomeFormValues>({
    resolver: zodResolver(createBusinessOutcomeSchema),
    defaultValues: {
      name: "",
      description: "",
      hypothesis: "",
      owner_id: "",
      target_date: "",
      baseline_value: "",
      target_value: "",
      current_value: "",
      confidence_score: "",
      financial_impact_estimate: "",
    },
  });

  useEffect(() => {
    if (!open) return;
    reset({
      name: "",
      description: "",
      hypothesis: "",
      owner_id: "",
      target_date: "",
      baseline_value: "",
      target_value: "",
      current_value: "",
      confidence_score: "",
      financial_impact_estimate: "",
    });
  }, [open, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    try {
      const input: CreateBusinessOutcomeInput = {
        name: values.name.trim(),
        description: emptyToNull(values.description),
        hypothesis: emptyToNull(values.hypothesis),
        owner_id: values.owner_id ? values.owner_id : null,
        target_date: emptyToNull(values.target_date),
        baseline_value: emptyToNull(values.baseline_value),
        target_value: emptyToNull(values.target_value),
        current_value: emptyToNull(values.current_value),
        confidence_score: emptyToNull(values.confidence_score),
        financial_impact_estimate: emptyToNull(values.financial_impact_estimate),
      };
      await onSubmit(input);
      toast({ title: "Business outcome created", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not create outcome",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Create business outcome"
      description="Define a measurable outcome to trace engineering work against."
      maxWidthClassName="max-w-2xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="bo-create-name">Name</Label>
          <Input
            id="bo-create-name"
            placeholder="e.g. Increase Monthly Active Users"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="bo-create-description">Description</Label>
          <textarea
            id="bo-create-description"
            rows={3}
            {...register("description")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="What does success look like?"
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="bo-create-hypothesis">Hypothesis</Label>
          <textarea
            id="bo-create-hypothesis"
            rows={2}
            {...register("hypothesis")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="Why do we believe delivering this drives the outcome?"
          />
          {errors.hypothesis && (
            <p className="text-xs text-destructive">
              {errors.hypothesis.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="bo-create-owner">Owner</Label>
            <select
              id="bo-create-owner"
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
            <Label htmlFor="bo-create-target-date">Target date</Label>
            <Input
              id="bo-create-target-date"
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
            <Label htmlFor="bo-create-baseline">Baseline value</Label>
            <Input
              id="bo-create-baseline"
              inputMode="decimal"
              placeholder="e.g. 1000"
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
            <Label htmlFor="bo-create-target">Target value</Label>
            <Input
              id="bo-create-target"
              inputMode="decimal"
              placeholder="e.g. 1500"
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
            <Label htmlFor="bo-create-current">Current value</Label>
            <Input
              id="bo-create-current"
              inputMode="decimal"
              placeholder="e.g. 1150"
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
            <Label htmlFor="bo-create-confidence">Confidence score (%)</Label>
            <Input
              id="bo-create-confidence"
              inputMode="decimal"
              placeholder="0 – 100"
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
            <Label htmlFor="bo-create-impact">Financial impact estimate</Label>
            <Input
              id="bo-create-impact"
              inputMode="decimal"
              placeholder="e.g. 250000"
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
          <Button type="submit" disabled={submitting}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Creating…
              </>
            ) : (
              "Create outcome"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
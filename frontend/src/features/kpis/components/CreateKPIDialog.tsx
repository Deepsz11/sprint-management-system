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
  KPI_DIRECTION_OPTIONS,
  KPI_UNIT_OPTIONS,
  createKPISchema,
  emptyToNull,
  type CreateKPIFormValues,
} from "../kpiSchemas";
import type {
  CreateKPIInput,
  KPIDirection,
  KPIOutcomeOption,
  KPIOwnerOption,
  KPIUnit,
} from "../types";
import { Modal } from "./Modal";

interface CreateKPIDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: CreateKPIInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly outcomes: KPIOutcomeOption[];
  readonly owners: KPIOwnerOption[];
  readonly outcomesLoading: boolean;
  readonly ownersLoading: boolean;
  readonly defaultOutcomeId: string | null;
}

const UNIT_LABELS: Record<KPIUnit, string> = {
  currency: "Currency",
  percent: "Percent",
  count: "Number",
  ratio: "Ratio",
  duration_seconds: "Duration (seconds)",
  duration_days: "Duration (days)",
  score: "Score",
};

const DIRECTION_LABELS: Record<KPIDirection, string> = {
  increase: "Increase",
  decrease: "Decrease",
  maintain: "Maintain",
};

function frequencyValue(
  refreshHours: number | undefined,
): number | undefined {
  return typeof refreshHours === "number" ? refreshHours : undefined;
}

export function CreateKPIDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
  outcomes,
  owners,
  outcomesLoading,
  ownersLoading,
  defaultOutcomeId,
}: CreateKPIDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    watch,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CreateKPIFormValues>({
    resolver: zodResolver(createKPISchema),
    defaultValues: {
      outcome_id: defaultOutcomeId ?? "",
      owner_id: "",
      name: "",
      description: "",
      unit: "count",
      currency: "",
      direction: "increase",
      baseline_value: "",
      target_value: "",
      current_value: "",
      data_source: "",
      refresh_frequency_hours: "",
    },
  });

  useEffect(() => {
    if (!open) return;
    reset({
      outcome_id: defaultOutcomeId ?? "",
      owner_id: "",
      name: "",
      description: "",
      unit: "count",
      currency: "",
      direction: "increase",
      baseline_value: "",
      target_value: "",
      current_value: "",
      data_source: "",
      refresh_frequency_hours: "",
    });
  }, [open, defaultOutcomeId, reset]);

  const watchedUnit = watch("unit");
  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    try {
      const refresh = frequencyValue(
        typeof values.refresh_frequency_hours === "number"
          ? values.refresh_frequency_hours
          : undefined,
      );
      const input: CreateKPIInput = {
        outcome_id: values.outcome_id ? values.outcome_id : null,
        owner_id: values.owner_id ? values.owner_id : null,
        name: values.name.trim(),
        description: emptyToNull(values.description),
        unit: values.unit,
        currency: values.unit === "currency" ? emptyToNull(values.currency) : null,
        direction: values.direction,
        baseline_value: emptyToNull(values.baseline_value),
        target_value: emptyToNull(values.target_value),
        current_value: emptyToNull(values.current_value),
        data_source: emptyToNull(values.data_source),
        refresh_frequency_hours: refresh ?? null,
      };
      await onSubmit(input);
      toast({ title: "KPI created", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not create KPI",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Create KPI"
      description="Define a measurable indicator tied to a business outcome."
      maxWidthClassName="max-w-2xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="kpi-create-outcome">Business outcome</Label>
            <select
              id="kpi-create-outcome"
              {...register("outcome_id")}
              disabled={outcomesLoading}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <option value="">
                {outcomesLoading ? "Loading…" : "Organization-wide"}
              </option>
              {outcomes.map((outcome) => (
                <option key={outcome.id} value={outcome.id}>
                  {outcome.name}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="kpi-create-owner">Owner</Label>
            <select
              id="kpi-create-owner"
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
        </div>

        <div className="space-y-2">
          <Label htmlFor="kpi-create-name">Name</Label>
          <Input
            id="kpi-create-name"
            placeholder="e.g. Monthly Active Users"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="kpi-create-description">Description</Label>
          <textarea
            id="kpi-create-description"
            rows={3}
            {...register("description")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="How is this metric defined and computed?"
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <Label htmlFor="kpi-create-unit">Metric type</Label>
            <select
              id="kpi-create-unit"
              {...register("unit")}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {KPI_UNIT_OPTIONS.map((unit) => (
                <option key={unit} value={unit}>
                  {UNIT_LABELS[unit]}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="kpi-create-direction">Direction</Label>
            <select
              id="kpi-create-direction"
              {...register("direction")}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {KPI_DIRECTION_OPTIONS.map((direction) => (
                <option key={direction} value={direction}>
                  {DIRECTION_LABELS[direction]}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="kpi-create-currency">Currency</Label>
            <Input
              id="kpi-create-currency"
              placeholder="USD"
              maxLength={3}
              disabled={watchedUnit !== "currency"}
              {...register("currency")}
              aria-invalid={Boolean(errors.currency)}
            />
            {errors.currency && (
              <p className="text-xs text-destructive">
                {errors.currency.message}
              </p>
            )}
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <Label htmlFor="kpi-create-baseline">Baseline value</Label>
            <Input
              id="kpi-create-baseline"
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
            <Label htmlFor="kpi-create-target">Target value</Label>
            <Input
              id="kpi-create-target"
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
            <Label htmlFor="kpi-create-current">Current value</Label>
            <Input
              id="kpi-create-current"
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
            <Label htmlFor="kpi-create-source">Data source</Label>
            <Input
              id="kpi-create-source"
              placeholder="e.g. analytics.mau_daily"
              {...register("data_source")}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="kpi-create-frequency">
              Refresh frequency (hours)
            </Label>
            <Input
              id="kpi-create-frequency"
              type="number"
              min={1}
              step={1}
              placeholder="24"
              {...register("refresh_frequency_hours")}
              aria-invalid={Boolean(errors.refresh_frequency_hours)}
            />
            {errors.refresh_frequency_hours && (
              <p className="text-xs text-destructive">
                {errors.refresh_frequency_hours.message}
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
              "Create KPI"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
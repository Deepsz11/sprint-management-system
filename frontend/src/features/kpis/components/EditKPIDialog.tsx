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
  editKPISchema,
  emptyToNull,
  type EditKPIFormValues,
} from "../kpiSchemas";
import type {
  KPI,
  KPIDirection,
  KPIOutcomeOption,
  KPIOwnerOption,
  UpdateKPIInput,
} from "../types";
import { Modal } from "./Modal";

interface EditKPIDialogProps {
  readonly open: boolean;
  readonly kpi: KPI | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: UpdateKPIInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly outcomes: KPIOutcomeOption[];
  readonly owners: KPIOwnerOption[];
  readonly outcomesLoading: boolean;
  readonly ownersLoading: boolean;
}

const DIRECTION_LABELS: Record<KPIDirection, string> = {
  increase: "Increase",
  decrease: "Decrease",
  maintain: "Maintain",
};

function toStringOrEmpty(
  value: string | number | null | undefined,
): string {
  if (value === null || value === undefined) return "";
  return String(value);
}

export function EditKPIDialog({
  open,
  kpi,
  onClose,
  onSubmit,
  isSubmitting,
  outcomes,
  owners,
  outcomesLoading,
  ownersLoading,
}: EditKPIDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditKPIFormValues>({
    resolver: zodResolver(editKPISchema),
    defaultValues: {
      outcome_id: "",
      owner_id: "",
      name: "",
      description: "",
      direction: "increase",
      baseline_value: "",
      target_value: "",
      current_value: "",
      data_source: "",
      refresh_frequency_hours: "",
      is_active: true,
    },
  });

  useEffect(() => {
    if (open && kpi) {
      reset({
        outcome_id: kpi.outcome_id ?? "",
        owner_id: kpi.owner_id ?? "",
        name: kpi.name,
        description: kpi.description ?? "",
        direction: kpi.direction,
        baseline_value: toStringOrEmpty(kpi.baseline_value),
        target_value: toStringOrEmpty(kpi.target_value),
        current_value: toStringOrEmpty(kpi.current_value),
        data_source: kpi.data_source ?? "",
        refresh_frequency_hours: toStringOrEmpty(kpi.refresh_frequency_hours),
        is_active: kpi.is_active,
      });
    }
  }, [open, kpi, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!kpi) return;
    try {
      const refresh =
        typeof values.refresh_frequency_hours === "number"
          ? values.refresh_frequency_hours
          : null;
      const input: UpdateKPIInput = {
        outcome_id: values.outcome_id ? values.outcome_id : null,
        owner_id: values.owner_id ? values.owner_id : null,
        name: values.name.trim(),
        description: emptyToNull(values.description),
        direction: values.direction,
        baseline_value: emptyToNull(values.baseline_value),
        target_value: emptyToNull(values.target_value),
        current_value: emptyToNull(values.current_value),
        data_source: emptyToNull(values.data_source),
        refresh_frequency_hours: refresh,
        is_active: values.is_active,
      };
      await onSubmit(kpi.id, input);
      toast({ title: "KPI updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update KPI",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && kpi !== null}
      onClose={onClose}
      title={`Edit ${kpi?.name ?? "KPI"}`}
      description={kpi ? `Metric type: ${kpi.unit}` : undefined}
      maxWidthClassName="max-w-2xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="kpi-edit-outcome">Business outcome</Label>
            <select
              id="kpi-edit-outcome"
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
            <Label htmlFor="kpi-edit-owner">Owner</Label>
            <select
              id="kpi-edit-owner"
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
          <Label htmlFor="kpi-edit-name">Name</Label>
          <Input
            id="kpi-edit-name"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="kpi-edit-description">Description</Label>
          <textarea
            id="kpi-edit-description"
            rows={3}
            {...register("description")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <Label htmlFor="kpi-edit-direction">Direction</Label>
            <select
              id="kpi-edit-direction"
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
            <Label htmlFor="kpi-edit-baseline">Baseline value</Label>
            <Input
              id="kpi-edit-baseline"
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
            <Label htmlFor="kpi-edit-target">Target value</Label>
            <Input
              id="kpi-edit-target"
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
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <Label htmlFor="kpi-edit-current">Current value</Label>
            <Input
              id="kpi-edit-current"
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
          <div className="space-y-2">
            <Label htmlFor="kpi-edit-source">Data source</Label>
            <Input id="kpi-edit-source" {...register("data_source")} />
          </div>
          <div className="space-y-2">
            <Label htmlFor="kpi-edit-frequency">Refresh (hours)</Label>
            <Input
              id="kpi-edit-frequency"
              type="number"
              min={1}
              step={1}
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

        <label className="inline-flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            className="h-4 w-4 rounded border-input text-primary focus:ring-2 focus:ring-ring"
            {...register("is_active")}
          />
          Active
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
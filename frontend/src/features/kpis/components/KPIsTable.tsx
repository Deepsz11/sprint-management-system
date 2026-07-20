import { Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type {
  KPI,
  KPIOutcomeOption,
  KPIOwnerOption,
  KPIUnit,
} from "../types";
import { KPIStatusBadge } from "./KPIStatusBadge";

interface KPIsTableProps {
  readonly kpis: KPI[];
  readonly outcomes: KPIOutcomeOption[];
  readonly owners: KPIOwnerOption[];
  readonly isMutating: boolean;
  readonly onEdit: (kpi: KPI) => void;
  readonly onDelete: (kpi: KPI) => void;
}

function toNumber(value: string | number | null | undefined): number | null {
  if (value === null || value === undefined) return null;
  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function formatValue(
  value: string | number | null | undefined,
  unit: KPIUnit,
  currency: string | null,
): string {
  const parsed = toNumber(value);
  if (parsed === null) return "—";
  if (unit === "currency") {
    try {
      return new Intl.NumberFormat(undefined, {
        style: "currency",
        currency: currency ?? "USD",
        maximumFractionDigits: 2,
      }).format(parsed);
    } catch {
      return `${parsed.toLocaleString()} ${currency ?? ""}`.trim();
    }
  }
  if (unit === "percent") {
    return `${parsed.toLocaleString(undefined, {
      maximumFractionDigits: 2,
    })}%`;
  }
  if (unit === "duration_seconds") {
    return `${parsed.toLocaleString()} s`;
  }
  if (unit === "duration_days") {
    return `${parsed.toLocaleString()} d`;
  }
  return parsed.toLocaleString(undefined, { maximumFractionDigits: 4 });
}

function formatFrequency(value: number | null): string {
  if (value === null || value === undefined) return "—";
  if (value >= 24 * 90) return "Quarterly";
  if (value >= 24 * 28) return "Monthly";
  if (value >= 24 * 7) return "Weekly";
  if (value >= 24) return "Daily";
  return `${value}h`;
}

export function KPIsTable({
  kpis,
  outcomes,
  owners,
  isMutating,
  onEdit,
  onDelete,
}: KPIsTableProps) {
  const outcomeMap = new Map(
    outcomes.map((outcome) => [outcome.id, outcome.name]),
  );
  const ownerMap = new Map(owners.map((owner) => [owner.id, owner.full_name]));

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                KPI
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Business outcome
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Owner
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Current
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Target
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Status
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Refresh
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {kpis.map((kpi) => (
              <tr
                key={kpi.id}
                className={cn(
                  "transition-colors hover:bg-muted/30",
                  !kpi.is_active && "opacity-70",
                )}
              >
                <td className="px-4 py-3">
                  <div className="flex flex-col">
                    <span className="font-medium text-foreground">
                      {kpi.name}
                    </span>
                    {kpi.description && (
                      <span className="line-clamp-1 text-xs text-muted-foreground">
                        {kpi.description}
                      </span>
                    )}
                  </div>
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {kpi.outcome_id
                    ? outcomeMap.get(kpi.outcome_id) ?? "—"
                    : "Organization-wide"}
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {kpi.owner_id
                    ? ownerMap.get(kpi.owner_id) ?? "—"
                    : "Unassigned"}
                </td>
                <td className="px-4 py-3 text-foreground">
                  {formatValue(kpi.current_value, kpi.unit, kpi.currency)}
                </td>
                <td className="px-4 py-3 text-foreground">
                  {formatValue(kpi.target_value, kpi.unit, kpi.currency)}
                </td>
                <td className="px-4 py-3">
                  <KPIStatusBadge kpi={kpi} />
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {formatFrequency(kpi.refresh_frequency_hours)}
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center justify-end gap-1">
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={`Edit ${kpi.name}`}
                      onClick={() => onEdit(kpi)}
                      disabled={isMutating}
                      title="Edit KPI"
                    >
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={`Delete ${kpi.name}`}
                      onClick={() => onDelete(kpi)}
                      disabled={isMutating}
                      title="Delete KPI"
                      className="text-destructive hover:bg-destructive/10 hover:text-destructive"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
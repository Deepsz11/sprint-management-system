import { Search } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

import type {
  KPIOutcomeOption,
  KPIOwnerOption,
  KPIUnit,
} from "../types";
import { KPI_UNIT_OPTIONS } from "../kpiSchemas";

const UNIT_LABELS: Record<KPIUnit, string> = {
  currency: "Currency",
  percent: "Percent",
  count: "Number",
  ratio: "Ratio",
  duration_seconds: "Duration (seconds)",
  duration_days: "Duration (days)",
  score: "Score",
};

interface KPIFiltersProps {
  readonly outcomes: KPIOutcomeOption[];
  readonly owners: KPIOwnerOption[];
  readonly isLoadingOutcomes: boolean;
  readonly isLoadingOwners: boolean;
  readonly outcomeId: string | null;
  readonly ownerId: string | null;
  readonly units: readonly KPIUnit[];
  readonly isActive: boolean | null;
  readonly search: string;
  readonly onOutcomeChange: (value: string | null) => void;
  readonly onOwnerChange: (value: string | null) => void;
  readonly onUnitChange: (value: KPIUnit | "") => void;
  readonly onActiveChange: (value: boolean | null) => void;
  readonly onSearchChange: (value: string) => void;
  readonly onReset: () => void;
}

export function KPIFilters({
  outcomes,
  owners,
  isLoadingOutcomes,
  isLoadingOwners,
  outcomeId,
  ownerId,
  units,
  isActive,
  search,
  onOutcomeChange,
  onOwnerChange,
  onUnitChange,
  onActiveChange,
  onSearchChange,
  onReset,
}: KPIFiltersProps) {
  const activeUnit = units[0] ?? "";
  const activeStatus =
    isActive === null ? "" : isActive ? "active" : "inactive";

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card p-4">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="space-y-2">
          <Label htmlFor="kpi-outcome">Business outcome</Label>
          <select
            id="kpi-outcome"
            value={outcomeId ?? ""}
            onChange={(event) =>
              onOutcomeChange(event.target.value ? event.target.value : null)
            }
            disabled={isLoadingOutcomes}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">
              {isLoadingOutcomes ? "Loading…" : "All outcomes"}
            </option>
            {outcomes.map((outcome) => (
              <option key={outcome.id} value={outcome.id}>
                {outcome.name}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="kpi-owner">Owner</Label>
          <select
            id="kpi-owner"
            value={ownerId ?? ""}
            onChange={(event) =>
              onOwnerChange(event.target.value ? event.target.value : null)
            }
            disabled={isLoadingOwners}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">
              {isLoadingOwners ? "Loading…" : "All owners"}
            </option>
            {owners.map((owner) => (
              <option key={owner.id} value={owner.id}>
                {owner.full_name}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="kpi-unit">Unit / Metric type</Label>
          <select
            id="kpi-unit"
            value={activeUnit}
            onChange={(event) =>
              onUnitChange(event.target.value as KPIUnit | "")
            }
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">All types</option>
            {KPI_UNIT_OPTIONS.map((unit) => (
              <option key={unit} value={unit}>
                {UNIT_LABELS[unit]}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="kpi-active">Status</Label>
          <select
            id="kpi-active"
            value={activeStatus}
            onChange={(event) => {
              const value = event.target.value;
              if (value === "") onActiveChange(null);
              else if (value === "active") onActiveChange(true);
              else onActiveChange(false);
            }}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">All</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="relative w-full sm:max-w-md">
          <Search
            aria-hidden="true"
            className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
          />
          <Input
            type="search"
            placeholder="Search by name, description, or source…"
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            className="pl-9"
            aria-label="Search KPIs"
          />
        </div>
        <Button type="button" variant="outline" onClick={onReset}>
          Reset filters
        </Button>
      </div>
    </div>
  );
}
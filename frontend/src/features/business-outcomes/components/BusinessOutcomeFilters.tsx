import { Search } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

import type { OutcomeOwnerOption, OutcomeStatus } from "../types";
import { OUTCOME_STATUS_OPTIONS } from "../businessOutcomeSchemas";
import { OUTCOME_STATUS_LABELS } from "./BusinessOutcomeStatusBadge";

interface BusinessOutcomeFiltersProps {
  readonly owners: OutcomeOwnerOption[];
  readonly isLoadingOwners: boolean;
  readonly ownerId: string | null;
  readonly statuses: readonly OutcomeStatus[];
  readonly search: string;
  readonly targetBefore: string | null;
  readonly targetAfter: string | null;
  readonly onOwnerChange: (value: string | null) => void;
  readonly onStatusChange: (value: OutcomeStatus | "") => void;
  readonly onSearchChange: (value: string) => void;
  readonly onTargetBeforeChange: (value: string | null) => void;
  readonly onTargetAfterChange: (value: string | null) => void;
  readonly onReset: () => void;
}

export function BusinessOutcomeFilters({
  owners,
  isLoadingOwners,
  ownerId,
  statuses,
  search,
  targetBefore,
  targetAfter,
  onOwnerChange,
  onStatusChange,
  onSearchChange,
  onTargetBeforeChange,
  onTargetAfterChange,
  onReset,
}: BusinessOutcomeFiltersProps) {
  const activeStatus = statuses[0] ?? "";

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card p-4">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="space-y-2">
          <Label htmlFor="bo-owner">Owner</Label>
          <select
            id="bo-owner"
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
          <Label htmlFor="bo-status">Status</Label>
          <select
            id="bo-status"
            value={activeStatus}
            onChange={(event) =>
              onStatusChange(event.target.value as OutcomeStatus | "")
            }
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">All statuses</option>
            {OUTCOME_STATUS_OPTIONS.map((status) => (
              <option key={status} value={status}>
                {OUTCOME_STATUS_LABELS[status]}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="bo-target-after">Target after</Label>
          <Input
            id="bo-target-after"
            type="date"
            value={targetAfter ?? ""}
            onChange={(event) =>
              onTargetAfterChange(
                event.target.value ? event.target.value : null,
              )
            }
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="bo-target-before">Target before</Label>
          <Input
            id="bo-target-before"
            type="date"
            value={targetBefore ?? ""}
            onChange={(event) =>
              onTargetBeforeChange(
                event.target.value ? event.target.value : null,
              )
            }
          />
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
            placeholder="Search by name…"
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            className="pl-9"
            aria-label="Search business outcomes"
          />
        </div>
        <Button type="button" variant="outline" onClick={onReset}>
          Reset filters
        </Button>
      </div>
    </div>
  );
}
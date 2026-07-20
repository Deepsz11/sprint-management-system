import { Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type {
  BusinessOutcome,
  OutcomeOwnerOption,
  OutcomeProjectOption,
} from "../types";
import { BusinessOutcomeStatusBadge } from "./BusinessOutcomeStatusBadge";

interface BusinessOutcomesTableProps {
  readonly outcomes: BusinessOutcome[];
  readonly projects: OutcomeProjectOption[];
  readonly owners: OutcomeOwnerOption[];
  readonly isMutating: boolean;
  readonly onEdit: (outcome: BusinessOutcome) => void;
  readonly onDelete: (outcome: BusinessOutcome) => void;
}

function toNumber(value: string | number | null | undefined): number | null {
  if (value === null || value === undefined) return null;
  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function formatNumber(value: string | number | null | undefined): string {
  const parsed = toNumber(value);
  if (parsed === null) return "—";
  return parsed.toLocaleString(undefined, {
    maximumFractionDigits: 4,
  });
}

function formatPercent(value: string | number | null | undefined): string {
  const parsed = toNumber(value);
  if (parsed === null) return "—";
  return `${Math.max(0, Math.min(100, Math.round(parsed)))}%`;
}

function formatDate(value: string | null): string {
  if (!value) return "—";
  const parsed = Date.parse(value);
  if (Number.isNaN(parsed)) return value;
  return new Date(parsed).toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "2-digit",
  });
}

export function BusinessOutcomesTable({
  outcomes,
  projects,
  owners,
  isMutating,
  onEdit,
  onDelete,
}: BusinessOutcomesTableProps) {
  const projectMap = new Map(
    projects.map((project) => [project.id, `${project.name} (${project.key})`]),
  );
  const ownerMap = new Map(owners.map((owner) => [owner.id, owner.full_name]));

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Title
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Project
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Owner
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Status
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Progress
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Target value
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Target date
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {outcomes.map((outcome) => {
              const canDelete = outcome.status !== "abandoned";
              return (
                <tr
                  key={outcome.id}
                  className={cn(
                    "transition-colors hover:bg-muted/30",
                    outcome.status === "abandoned" && "opacity-70",
                  )}
                >
                  <td className="px-4 py-3">
                    <div className="flex flex-col">
                      <span className="font-medium text-foreground">
                        {outcome.name}
                      </span>
                      {outcome.description && (
                        <span className="line-clamp-1 text-xs text-muted-foreground">
                          {outcome.description}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {projectMap.get(outcome.organization_id) ?? "Organization-wide"}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {outcome.owner_id
                      ? ownerMap.get(outcome.owner_id) ?? "—"
                      : "Unassigned"}
                  </td>
                  <td className="px-4 py-3">
                    <BusinessOutcomeStatusBadge status={outcome.status} />
                  </td>
                  <td className="px-4 py-3 text-foreground">
                    <div className="flex flex-col">
                      <span>{formatPercent(outcome.progress_percent)}</span>
                      <span className="text-xs text-muted-foreground">
                        {formatNumber(outcome.current_value)} /{" "}
                        {formatNumber(outcome.target_value)}
                      </span>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-foreground">
                    {formatNumber(outcome.target_value)}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {formatDate(outcome.target_date)}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center justify-end gap-1">
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Edit ${outcome.name}`}
                        onClick={() => onEdit(outcome)}
                        disabled={isMutating}
                        title="Edit outcome"
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Delete ${outcome.name}`}
                        onClick={() => onDelete(outcome)}
                        disabled={isMutating || !canDelete}
                        title={
                          canDelete
                            ? "Delete outcome"
                            : "Abandoned outcomes cannot be deleted from the table"
                        }
                        className="text-destructive hover:bg-destructive/10 hover:text-destructive disabled:text-muted-foreground"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
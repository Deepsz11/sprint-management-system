import { Building2, Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type { Organization } from "../types";

interface OrganizationsTableProps {
  readonly organizations: Organization[];
  readonly isMutating: boolean;
  readonly onEdit: (organization: Organization) => void;
  readonly onDelete: (organization: Organization) => void;
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

function statusBadgeClasses(isActive: boolean): string {
  return cn(
    "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
    isActive
      ? "border border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300"
      : "border border-border bg-muted text-muted-foreground",
  );
}

export function OrganizationsTable({
  organizations,
  isMutating,
  onEdit,
  onDelete,
}: OrganizationsTableProps) {
  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Organization
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Slug
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Billing email
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Status
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Created
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {organizations.map((organization) => (
              <tr
                key={organization.id}
                className={cn(
                  "transition-colors hover:bg-muted/30",
                  !organization.is_active && "opacity-70",
                )}
              >
                <td className="px-4 py-3">
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
                      <Building2 className="h-4 w-4" aria-hidden="true" />
                    </div>
                    <div className="flex flex-col">
                      <span className="font-medium text-foreground">
                        {organization.name}
                      </span>
                      {organization.description && (
                        <span className="line-clamp-1 text-xs text-muted-foreground">
                          {organization.description}
                        </span>
                      )}
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3 font-mono text-xs text-muted-foreground">
                  {organization.slug}
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {organization.billing_email ?? "—"}
                </td>
                <td className="px-4 py-3">
                  <span className={statusBadgeClasses(organization.is_active)}>
                    {organization.is_active ? "Active" : "Inactive"}
                  </span>
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {formatDate(organization.created_at)}
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center justify-end gap-1">
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={`Edit ${organization.name}`}
                      onClick={() => onEdit(organization)}
                      disabled={isMutating}
                      title="Edit organization"
                    >
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={`Delete ${organization.name}`}
                      onClick={() => onDelete(organization)}
                      disabled={isMutating}
                      title="Delete organization"
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
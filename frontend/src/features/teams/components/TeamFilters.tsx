import { Search } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

import type { TeamOrganizationOption } from "../types";
import type { TeamFilters as TeamFiltersState } from "../useTeams";

interface TeamFiltersProps {
  readonly organizations: TeamOrganizationOption[];
  readonly isLoadingOrganizations: boolean;
  readonly search: string;
  readonly organizationId: string | null;
  readonly status: TeamFiltersState["status"];
  readonly onSearchChange: (value: string) => void;
  readonly onOrganizationChange: (value: string | null) => void;
  readonly onStatusChange: (value: TeamFiltersState["status"]) => void;
  readonly onReset: () => void;
}

export function TeamFilters({
  organizations,
  isLoadingOrganizations,
  search,
  organizationId,
  status,
  onSearchChange,
  onOrganizationChange,
  onStatusChange,
  onReset,
}: TeamFiltersProps) {
  return (
    <div className="space-y-4 rounded-lg border border-border bg-card p-4">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div className="space-y-2 md:col-span-2">
          <Label htmlFor="team-search">Search</Label>
          <div className="relative">
            <Search
              aria-hidden="true"
              className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
            />
            <Input
              id="team-search"
              type="search"
              placeholder="Name, slug, or description…"
              value={search}
              onChange={(event) => onSearchChange(event.target.value)}
              className="pl-9"
              aria-label="Search teams"
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="team-org">Organization</Label>
          <select
            id="team-org"
            value={organizationId ?? ""}
            onChange={(event) =>
              onOrganizationChange(
                event.target.value ? event.target.value : null,
              )
            }
            disabled={isLoadingOrganizations}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">
              {isLoadingOrganizations ? "Loading…" : "All organizations"}
            </option>
            {organizations.map((organization) => (
              <option key={organization.id} value={organization.id}>
                {organization.name}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="team-status">Status</Label>
          <select
            id="team-status"
            value={status}
            onChange={(event) =>
              onStatusChange(event.target.value as TeamFiltersState["status"])
            }
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="all">All</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>
      </div>

      <div className="flex justify-end">
        <Button type="button" variant="outline" onClick={onReset}>
          Reset filters
        </Button>
      </div>
    </div>
  );
}
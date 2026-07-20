import { Search } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

import type { OrganizationFilters as OrganizationFiltersState } from "../useOrganizations";

interface OrganizationFiltersProps {
  readonly search: string;
  readonly status: OrganizationFiltersState["status"];
  readonly onSearchChange: (value: string) => void;
  readonly onStatusChange: (value: OrganizationFiltersState["status"]) => void;
  readonly onReset: () => void;
}

export function OrganizationFilters({
  search,
  status,
  onSearchChange,
  onStatusChange,
  onReset,
}: OrganizationFiltersProps) {
  return (
    <div className="space-y-4 rounded-lg border border-border bg-card p-4">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        <div className="space-y-2 md:col-span-2">
          <Label htmlFor="org-search">Search</Label>
          <div className="relative">
            <Search
              aria-hidden="true"
              className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
            />
            <Input
              id="org-search"
              type="search"
              placeholder="Name, slug, description, or email…"
              value={search}
              onChange={(event) => onSearchChange(event.target.value)}
              className="pl-9"
              aria-label="Search organizations"
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="org-status">Status</Label>
          <select
            id="org-status"
            value={status}
            onChange={(event) =>
              onStatusChange(
                event.target.value as OrganizationFiltersState["status"],
              )
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
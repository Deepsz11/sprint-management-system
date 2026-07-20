import { Search } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

import type {
  UserOrganizationOption,
  UserRole,
  UserStatus,
  UserTeamOption,
} from "../types";
import type { UserFilters as UserFiltersState } from "../useUsers";
import { ROLE_LABELS, useRoleOptions } from "../useRoleOptions";
import { USER_STATUS_OPTIONS } from "../userSchemas";
import { USER_STATUS_LABELS } from "./UserStatusBadge";

interface UserFiltersProps {
  readonly organizations: UserOrganizationOption[];
  readonly teams: UserTeamOption[];
  readonly isLoadingOrganizations: boolean;
  readonly isLoadingTeams: boolean;
  readonly search: string;
  readonly organizationId: string | null;
  readonly teamId: string | null;
  readonly role: UserRole | null;
  readonly status: UserFiltersState["status"];
  readonly onSearchChange: (value: string) => void;
  readonly onOrganizationChange: (value: string | null) => void;
  readonly onTeamChange: (value: string | null) => void;
  readonly onRoleChange: (value: UserRole | null) => void;
  readonly onStatusChange: (value: UserFiltersState["status"]) => void;
  readonly onReset: () => void;
}

export function UserFilters({
  organizations,
  teams,
  isLoadingOrganizations,
  isLoadingTeams,
  search,
  organizationId,
  teamId,
  role,
  status,
  onSearchChange,
  onOrganizationChange,
  onTeamChange,
  onRoleChange,
  onStatusChange,
  onReset,
}: UserFiltersProps) {
  const roleOptions = useRoleOptions();
  const filteredTeams = organizationId
    ? teams.filter((team) => team.organization_id === organizationId)
    : teams;

  return (
    <div className="space-y-4 rounded-lg border border-border bg-card p-4">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <div className="space-y-2 md:col-span-2 xl:col-span-2">
          <Label htmlFor="user-search">Search</Label>
          <div className="relative">
            <Search
              aria-hidden="true"
              className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
            />
            <Input
              id="user-search"
              type="search"
              placeholder="Name or email…"
              value={search}
              onChange={(event) => onSearchChange(event.target.value)}
              className="pl-9"
              aria-label="Search users"
            />
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="user-org">Organization</Label>
          <select
            id="user-org"
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
          <Label htmlFor="user-team">Team</Label>
          <select
            id="user-team"
            value={teamId ?? ""}
            onChange={(event) =>
              onTeamChange(event.target.value ? event.target.value : null)
            }
            disabled={isLoadingTeams || filteredTeams.length === 0}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">
              {isLoadingTeams
                ? "Loading…"
                : filteredTeams.length === 0
                ? "No teams available"
                : "All teams"}
            </option>
            {filteredTeams.map((team) => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="user-role">Role</Label>
          <select
            id="user-role"
            value={role ?? ""}
            onChange={(event) =>
              onRoleChange(
                event.target.value ? (event.target.value as UserRole) : null,
              )
            }
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">All roles</option>
            {roleOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {ROLE_LABELS[option.value]}
              </option>
            ))}
          </select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="user-status">Status</Label>
          <select
            id="user-status"
            value={status}
            onChange={(event) =>
              onStatusChange(event.target.value as UserFiltersState["status"])
            }
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="all">All</option>
            {USER_STATUS_OPTIONS.map((value) => (
              <option key={value} value={value}>
                {USER_STATUS_LABELS[value as UserStatus]}
              </option>
            ))}
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
import { Pencil, UserMinus } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type {
  User,
  UserOrganizationOption,
  UserTeamOption,
} from "../types";
import { RoleBadge } from "./RoleBadge";
import { UserStatusBadge } from "./UserStatusBadge";

interface UsersTableProps {
  readonly users: User[];
  readonly organizations: UserOrganizationOption[];
  readonly teams: UserTeamOption[];
  readonly isMutating: boolean;
  readonly onEdit: (user: User) => void;
  readonly onDeactivate: (user: User) => void;
  readonly teamByUserId?: Record<string, string | null>;
}

function initials(name: string): string {
  return name
    .split(/\s+/)
    .map((part) => part[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();
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

export function UsersTable({
  users,
  organizations,
  teams,
  isMutating,
  onEdit,
  onDeactivate,
  teamByUserId,
}: UsersTableProps) {
  const organizationMap = new Map(
    organizations.map((organization) => [organization.id, organization.name]),
  );
  const teamMap = new Map(teams.map((team) => [team.id, team.name]));

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                User
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Email
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Organization
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Team
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Role
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Status
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Last login
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {users.map((user) => {
              const teamId = teamByUserId?.[user.id] ?? null;
              const canDeactivate = user.status !== "deactivated";
              return (
                <tr
                  key={user.id}
                  className={cn(
                    "transition-colors hover:bg-muted/30",
                    user.status === "deactivated" && "opacity-70",
                  )}
                >
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
                        {initials(user.full_name)}
                      </div>
                      <div className="flex flex-col">
                        <span className="font-medium text-foreground">
                          {user.full_name}
                        </span>
                        {!user.is_email_verified && (
                          <span className="text-xs text-muted-foreground">
                            Email unverified
                          </span>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {user.email}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {user.organization_id
                      ? organizationMap.get(user.organization_id) ?? "—"
                      : "—"}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {teamId ? teamMap.get(teamId) ?? "—" : "—"}
                  </td>
                  <td className="px-4 py-3">
                    <RoleBadge role={user.role} />
                  </td>
                  <td className="px-4 py-3">
                    <UserStatusBadge status={user.status} />
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {formatDate(user.last_login_at)}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center justify-end gap-1">
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Edit ${user.full_name}`}
                        onClick={() => onEdit(user)}
                        disabled={isMutating}
                        title="Edit user"
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Deactivate ${user.full_name}`}
                        onClick={() => onDeactivate(user)}
                        disabled={isMutating || !canDeactivate}
                        title={
                          canDeactivate
                            ? "Deactivate user"
                            : "User is already deactivated"
                        }
                        className="text-destructive hover:bg-destructive/10 hover:text-destructive disabled:text-muted-foreground"
                      >
                        <UserMinus className="h-4 w-4" />
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
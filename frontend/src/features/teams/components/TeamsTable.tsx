import { Pencil, Trash2, Users2 } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type { Team, TeamLeadOption, TeamOrganizationOption } from "../types";
import { TeamStatusBadge } from "./TeamStatusBadge";

interface TeamsTableProps {
  readonly teams: Team[];
  readonly organizations: TeamOrganizationOption[];
  readonly leads: TeamLeadOption[];
  readonly isMutating: boolean;
  readonly onEdit: (team: Team) => void;
  readonly onDelete: (team: Team) => void;
  readonly leadByTeamId?: Record<string, string | null>;
  readonly memberCountByTeamId?: Record<string, number>;
  readonly activeByTeamId?: Record<string, boolean>;
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

export function TeamsTable({
  teams,
  organizations,
  leads,
  isMutating,
  onEdit,
  onDelete,
  leadByTeamId,
  memberCountByTeamId,
  activeByTeamId,
}: TeamsTableProps) {
  const organizationMap = new Map(
    organizations.map((organization) => [organization.id, organization.name]),
  );
  const leadMap = new Map(leads.map((lead) => [lead.id, lead.full_name]));

  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Team
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Organization
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Team lead
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Members
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
            {teams.map((team) => {
              const leadId = leadByTeamId?.[team.id] ?? null;
              const memberCount = memberCountByTeamId?.[team.id] ?? 0;
              const isActive = activeByTeamId?.[team.id] ?? true;

              return (
                <tr
                  key={team.id}
                  className={cn(
                    "transition-colors hover:bg-muted/30",
                    !isActive && "opacity-70",
                  )}
                >
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md bg-primary/10 text-primary">
                        <Users2 className="h-4 w-4" aria-hidden="true" />
                      </div>
                      <div className="flex flex-col">
                        <span className="font-medium text-foreground">
                          {team.name}
                        </span>
                        {team.description && (
                          <span className="line-clamp-1 text-xs text-muted-foreground">
                            {team.description}
                          </span>
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {organizationMap.get(team.organization_id) ?? "—"}
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {leadId ? leadMap.get(leadId) ?? "—" : "Unassigned"}
                  </td>
                  <td className="px-4 py-3 text-foreground">{memberCount}</td>
                  <td className="px-4 py-3">
                    <TeamStatusBadge isActive={isActive} />
                  </td>
                  <td className="px-4 py-3 text-muted-foreground">
                    {formatDate(team.created_at)}
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex items-center justify-end gap-1">
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Edit ${team.name}`}
                        onClick={() => onEdit(team)}
                        disabled={isMutating}
                        title="Edit team"
                      >
                        <Pencil className="h-4 w-4" />
                      </Button>
                      <Button
                        type="button"
                        variant="ghost"
                        size="icon"
                        aria-label={`Delete ${team.name}`}
                        onClick={() => onDelete(team)}
                        disabled={isMutating}
                        title="Delete team"
                        className="text-destructive hover:bg-destructive/10 hover:text-destructive"
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
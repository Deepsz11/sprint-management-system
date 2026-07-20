import { Plus } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  CreateTeamDialog,
  DeleteTeamDialog,
  EditTeamDialog,
  TeamFilters,
  TeamsErrorState,
  TeamsLoadingState,
  TeamsPagination,
  TeamsTable,
  useOrganizationOptions,
  useTeamLeadOptions,
  useTeams,
  type Team,
} from "@/features/teams";

const PAGE_SIZE = 20;

export default function TeamsPage() {
  const {
    data,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    filters,
    setSearch,
    setOrganizationId,
    setStatus,
    setPage,
    resetFilters,
    refresh,
    createTeam,
    updateTeam,
    deleteTeam,
  } = useTeams({ limit: PAGE_SIZE });

  const {
    organizations,
    isLoading: orgsLoading,
  } = useOrganizationOptions();
  const { leads, isLoading: leadsLoading } = useTeamLeadOptions();

  const [isCreateOpen, setCreateOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<Team | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Team | null>(null);
  const [teamLeadMap, setTeamLeadMap] = useState<Record<string, string | null>>(
    {},
  );
  const [teamActiveMap, setTeamActiveMap] = useState<Record<string, boolean>>(
    {},
  );

  const totalCount = data?.total ?? 0;
  const filtersActive =
    filters.search.trim().length > 0 ||
    filters.organizationId !== null ||
    filters.status !== "all";

  const isTeamActive = (team: Team) =>
    teamActiveMap[team.id] === undefined ? true : teamActiveMap[team.id];

  const visible = filtered.filter((team) => {
    if (filters.status === "all") return true;
    if (filters.status === "active") return isTeamActive(team);
    return !isTeamActive(team);
  });

  const hasResults = visible.length > 0;

  const activeMap = filtered.reduce<Record<string, boolean>>(
    (acc, team) => {
      acc[team.id] = isTeamActive(team);
      return acc;
    },
    {},
  );

  const handleLeadAssign = (teamId: string, leadId: string | null) => {
    setTeamLeadMap((current) => ({ ...current, [teamId]: leadId }));
  };

  const handleActiveChange = (teamId: string, isActive: boolean) => {
    setTeamActiveMap((current) => ({ ...current, [teamId]: isActive }));
  };

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Teams</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Organize people into teams and connect them to projects and outcomes.
          </p>
        </div>
        <Button type="button" onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4" />
          New team
        </Button>
      </header>

      <TeamFilters
        organizations={organizations}
        isLoadingOrganizations={orgsLoading}
        search={filters.search}
        organizationId={filters.organizationId}
        status={filters.status}
        onSearchChange={setSearch}
        onOrganizationChange={setOrganizationId}
        onStatusChange={setStatus}
        onReset={resetFilters}
      />

      {isLoading && !data ? (
        <TeamsLoadingState />
      ) : error ? (
        <TeamsErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            filtersActive ? "No teams match your filters" : "No teams yet"
          }
          description={
            filtersActive
              ? "Try broadening the search or clearing filters."
              : "Create your first team to start organizing delivery."
          }
          action={
            <div className="flex items-center gap-2">
              {filtersActive && (
                <Button
                  type="button"
                  variant="outline"
                  onClick={resetFilters}
                >
                  Reset filters
                </Button>
              )}
              <Button type="button" onClick={() => setCreateOpen(true)}>
                <Plus className="h-4 w-4" />
                New team
              </Button>
            </div>
          }
        />
      ) : (
        <div className="space-y-4">
          <TeamsTable
            teams={visible}
            organizations={organizations}
            leads={leads}
            isMutating={isMutating}
            leadByTeamId={teamLeadMap}
            activeByTeamId={activeMap}
            onEdit={setEditTarget}
            onDelete={setDeleteTarget}
          />
          <TeamsPagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <CreateTeamDialog
        open={isCreateOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={async (input) => {
          await createTeam(input);
        }}
        isSubmitting={isMutating}
        leads={leads}
        leadsLoading={leadsLoading}
        onLeadAssign={handleLeadAssign}
      />

      <EditTeamDialog
        open={editTarget !== null}
        team={editTarget}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateTeam(id, input);
        }}
        isSubmitting={isMutating}
        leads={leads}
        leadsLoading={leadsLoading}
        currentLeadId={editTarget ? teamLeadMap[editTarget.id] ?? null : null}
        currentIsActive={editTarget ? isTeamActive(editTarget) : true}
        onLeadChange={handleLeadAssign}
        onActiveChange={handleActiveChange}
      />

      <DeleteTeamDialog
        open={deleteTarget !== null}
        team={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={async (id) => {
          await deleteTeam(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
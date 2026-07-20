import { UserPlus } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  DeactivateUserDialog,
  EditUserDialog,
  InviteUserDialog,
  UserFilters,
  UsersErrorState,
  UsersLoadingState,
  UsersPagination,
  UsersTable,
  useOrganizationOptions,
  useTeamOptions,
  useUsers,
  type User,
} from "@/features/users";

const PAGE_SIZE = 20;

export default function UsersPage() {
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
    setTeamId,
    setRole,
    setStatus,
    setPage,
    resetFilters,
    refresh,
    inviteUser,
    updateUser,
    deactivateUser,
  } = useUsers({ limit: PAGE_SIZE });

  const {
    organizations,
    isLoading: orgsLoading,
  } = useOrganizationOptions();
  const { teams, isLoading: teamsLoading } = useTeamOptions();

  const [isInviteOpen, setInviteOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<User | null>(null);
  const [deactivateTarget, setDeactivateTarget] = useState<User | null>(null);
  const [teamByUserId, setTeamByUserId] = useState<
    Record<string, string | null>
  >({});

  const totalCount = data?.total ?? 0;
  const filtersActive =
    filters.search.trim().length > 0 ||
    filters.organizationId !== null ||
    filters.teamId !== null ||
    filters.role !== null ||
    filters.status !== "all";

  const visible = filtered.filter((user) => {
    if (!filters.teamId) return true;
    return teamByUserId[user.id] === filters.teamId;
  });

  const hasResults = visible.length > 0;

  const handleTeamAssign = (userId: string, teamId: string | null) => {
    setTeamByUserId((current) => ({ ...current, [userId]: teamId }));
  };

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Users</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage the people who can access this workspace.
          </p>
        </div>
        <Button type="button" onClick={() => setInviteOpen(true)}>
          <UserPlus className="h-4 w-4" />
          Invite user
        </Button>
      </header>

      <UserFilters
        organizations={organizations}
        teams={teams}
        isLoadingOrganizations={orgsLoading}
        isLoadingTeams={teamsLoading}
        search={filters.search}
        organizationId={filters.organizationId}
        teamId={filters.teamId}
        role={filters.role}
        status={filters.status}
        onSearchChange={setSearch}
        onOrganizationChange={setOrganizationId}
        onTeamChange={setTeamId}
        onRoleChange={setRole}
        onStatusChange={setStatus}
        onReset={resetFilters}
      />

      {isLoading && !data ? (
        <UsersLoadingState />
      ) : error ? (
        <UsersErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            filtersActive ? "No users match your filters" : "No users yet"
          }
          description={
            filtersActive
              ? "Try broadening the search or clearing filters."
              : "Invite your first user to start collaborating."
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
              <Button type="button" onClick={() => setInviteOpen(true)}>
                <UserPlus className="h-4 w-4" />
                Invite user
              </Button>
            </div>
          }
        />
      ) : (
        <div className="space-y-4">
          <UsersTable
            users={visible}
            organizations={organizations}
            teams={teams}
            isMutating={isMutating}
            onEdit={setEditTarget}
            onDeactivate={setDeactivateTarget}
            teamByUserId={teamByUserId}
          />
          <UsersPagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <InviteUserDialog
        open={isInviteOpen}
        onClose={() => setInviteOpen(false)}
        onSubmit={async (input) => {
          await inviteUser(input);
        }}
        isSubmitting={isMutating}
        organizations={organizations}
        teams={teams}
        orgsLoading={orgsLoading}
        teamsLoading={teamsLoading}
        defaultOrganizationId={filters.organizationId}
      />

      <EditUserDialog
        open={editTarget !== null}
        user={editTarget}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateUser(id, input);
        }}
        isSubmitting={isMutating}
        teams={teams}
        teamsLoading={teamsLoading}
        currentTeamId={editTarget ? teamByUserId[editTarget.id] ?? null : null}
        onTeamChange={handleTeamAssign}
      />

      <DeactivateUserDialog
        open={deactivateTarget !== null}
        user={deactivateTarget}
        onClose={() => setDeactivateTarget(null)}
        onConfirm={async (id) => {
          await deactivateUser(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
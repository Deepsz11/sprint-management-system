import { Plus } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  CreateOrganizationDialog,
  DeleteOrganizationDialog,
  EditOrganizationDialog,
  OrganizationFilters,
  OrganizationsErrorState,
  OrganizationsLoadingState,
  OrganizationsPagination,
  OrganizationsTable,
  useOrganizations,
  type Organization,
} from "@/features/organizations";

const PAGE_SIZE = 20;

export default function OrganizationsPage() {
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
    setStatus,
    setPage,
    resetFilters,
    refresh,
    createOrganization,
    updateOrganization,
    deleteOrganization,
  } = useOrganizations({ limit: PAGE_SIZE });

  const [isCreateOpen, setCreateOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<Organization | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Organization | null>(null);

  const totalCount = data?.total ?? 0;
  const hasResults = filtered.length > 0;
  const filtersActive =
    filters.search.trim().length > 0 || filters.status !== "all";

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Organizations
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage tenant organizations across the platform.
          </p>
        </div>
        <Button type="button" onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4" />
          New organization
        </Button>
      </header>

      <OrganizationFilters
        search={filters.search}
        status={filters.status}
        onSearchChange={setSearch}
        onStatusChange={setStatus}
        onReset={resetFilters}
      />

      {isLoading && !data ? (
        <OrganizationsLoadingState />
      ) : error ? (
        <OrganizationsErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            filtersActive
              ? "No organizations match your filters"
              : "No organizations yet"
          }
          description={
            filtersActive
              ? "Try broadening the search or clearing filters."
              : "Create your first organization to onboard a tenant."
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
                New organization
              </Button>
            </div>
          }
        />
      ) : (
        <div className="space-y-4">
          <OrganizationsTable
            organizations={filtered}
            isMutating={isMutating}
            onEdit={setEditTarget}
            onDelete={setDeleteTarget}
          />
          <OrganizationsPagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <CreateOrganizationDialog
        open={isCreateOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={async (input) => {
          await createOrganization(input);
        }}
        isSubmitting={isMutating}
      />

      <EditOrganizationDialog
        open={editTarget !== null}
        organization={editTarget}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateOrganization(id, input);
        }}
        isSubmitting={isMutating}
      />

      <DeleteOrganizationDialog
        open={deleteTarget !== null}
        organization={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={async (id) => {
          await deleteOrganization(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
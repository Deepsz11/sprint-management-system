import { Plus } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  BusinessOutcomeFilters,
  BusinessOutcomesErrorState,
  BusinessOutcomesLoadingState,
  BusinessOutcomesPagination,
  BusinessOutcomesTable,
  CreateBusinessOutcomeDialog,
  DeleteBusinessOutcomeDialog,
  EditBusinessOutcomeDialog,
  useBusinessOutcomes,
  useProjectOptions,
  type BusinessOutcome,
  type OutcomeStatus,
} from "@/features/business-outcomes";

const PAGE_SIZE = 20;

export default function BusinessOutcomesPage() {
  const {
    data,
    items,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    filters,
    setOwnerId,
    setStatuses,
    setSearch,
    setTargetBefore,
    setTargetAfter,
    setPage,
    resetFilters,
    refresh,
    createOutcome,
    updateOutcome,
    deleteOutcome,
  } = useBusinessOutcomes({ limit: PAGE_SIZE });

  const {
    projects,
    owners,
    isLoadingProjects,
    isLoadingOwners,
  } = useProjectOptions();

  const [isCreateOpen, setCreateOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<BusinessOutcome | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<BusinessOutcome | null>(
    null,
  );

  const handleStatus = (value: OutcomeStatus | "") => {
    setStatuses(value ? [value] : []);
  };

  const totalCount = data?.total ?? 0;
  const hasResults = items.length > 0;
  const filtersActive =
    filters.search.trim().length > 0 ||
    filters.ownerId !== null ||
    filters.statuses.length > 0 ||
    filters.targetBefore !== null ||
    filters.targetAfter !== null;

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Business outcomes
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Track the measurable outcomes engineering work is expected to drive.
          </p>
        </div>
        <Button type="button" onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4" />
          New outcome
        </Button>
      </header>

      <BusinessOutcomeFilters
        owners={owners}
        isLoadingOwners={isLoadingOwners}
        ownerId={filters.ownerId}
        statuses={filters.statuses}
        search={filters.search}
        targetBefore={filters.targetBefore}
        targetAfter={filters.targetAfter}
        onOwnerChange={setOwnerId}
        onStatusChange={handleStatus}
        onSearchChange={setSearch}
        onTargetBeforeChange={setTargetBefore}
        onTargetAfterChange={setTargetAfter}
        onReset={resetFilters}
      />

      {isLoading && !data ? (
        <BusinessOutcomesLoadingState />
      ) : error ? (
        <BusinessOutcomesErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            filtersActive
              ? "No outcomes match your filters"
              : "No business outcomes yet"
          }
          description={
            filtersActive
              ? "Try broadening the search or clearing filters."
              : "Create your first outcome to start tracing engineering work to business value."
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
                New outcome
              </Button>
            </div>
          }
        />
      ) : (
        <div className="space-y-4">
          <BusinessOutcomesTable
            outcomes={items}
            projects={projects}
            owners={owners}
            isMutating={isMutating}
            onEdit={setEditTarget}
            onDelete={setDeleteTarget}
          />
          <BusinessOutcomesPagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <CreateBusinessOutcomeDialog
        open={isCreateOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={async (input) => {
          await createOutcome(input);
        }}
        isSubmitting={isMutating}
        owners={owners}
        ownersLoading={isLoadingOwners || isLoadingProjects}
      />

      <EditBusinessOutcomeDialog
        open={editTarget !== null}
        outcome={editTarget}
        owners={owners}
        ownersLoading={isLoadingOwners}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateOutcome(id, input);
        }}
        isSubmitting={isMutating}
      />

      <DeleteBusinessOutcomeDialog
        open={deleteTarget !== null}
        outcome={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={async (id) => {
          await deleteOutcome(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
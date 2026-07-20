import { Plus } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  CreateKPIDialog,
  DeleteKPIDialog,
  EditKPIDialog,
  KPIFilters,
  KPIsErrorState,
  KPIsLoadingState,
  KPIsPagination,
  KPIsTable,
  useBusinessOutcomeOptions,
  useKPIs,
  useOwnerOptions,
  type KPI,
  type KPIUnit,
} from "@/features/kpis";

const PAGE_SIZE = 20;

export default function KPIsPage() {
  const {
    data,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    filters,
    setOutcomeId,
    setOwnerId,
    setUnits,
    setIsActive,
    setSearch,
    setPage,
    resetFilters,
    refresh,
    createKPI,
    updateKPI,
    deleteKPI,
  } = useKPIs({ limit: PAGE_SIZE });

  const {
    outcomes,
    isLoading: outcomesLoading,
  } = useBusinessOutcomeOptions();
  const { owners, isLoading: ownersLoading } = useOwnerOptions();

  const [isCreateOpen, setCreateOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<KPI | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<KPI | null>(null);

  const handleUnit = (value: KPIUnit | "") => {
    setUnits(value ? [value] : []);
  };

  const totalCount = data?.total ?? 0;
  const hasResults = filtered.length > 0;
  const filtersActive =
    filters.search.trim().length > 0 ||
    filters.outcomeId !== null ||
    filters.ownerId !== null ||
    filters.units.length > 0 ||
    filters.isActive !== null;

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">KPIs</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Track the indicators that measure business outcome performance.
          </p>
        </div>
        <Button type="button" onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4" />
          New KPI
        </Button>
      </header>

      <KPIFilters
        outcomes={outcomes}
        owners={owners}
        isLoadingOutcomes={outcomesLoading}
        isLoadingOwners={ownersLoading}
        outcomeId={filters.outcomeId}
        ownerId={filters.ownerId}
        units={filters.units}
        isActive={filters.isActive}
        search={filters.search}
        onOutcomeChange={setOutcomeId}
        onOwnerChange={setOwnerId}
        onUnitChange={handleUnit}
        onActiveChange={setIsActive}
        onSearchChange={setSearch}
        onReset={resetFilters}
      />

      {isLoading && !data ? (
        <KPIsLoadingState />
      ) : error ? (
        <KPIsErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            filtersActive ? "No KPIs match your filters" : "No KPIs yet"
          }
          description={
            filtersActive
              ? "Try broadening the search or clearing filters."
              : "Create your first KPI to start measuring business outcome progress."
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
                New KPI
              </Button>
            </div>
          }
        />
      ) : (
        <div className="space-y-4">
          <KPIsTable
            kpis={filtered}
            outcomes={outcomes}
            owners={owners}
            isMutating={isMutating}
            onEdit={setEditTarget}
            onDelete={setDeleteTarget}
          />
          <KPIsPagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <CreateKPIDialog
        open={isCreateOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={async (input) => {
          await createKPI(input);
        }}
        isSubmitting={isMutating}
        outcomes={outcomes}
        owners={owners}
        outcomesLoading={outcomesLoading}
        ownersLoading={ownersLoading}
        defaultOutcomeId={filters.outcomeId}
      />

      <EditKPIDialog
        open={editTarget !== null}
        kpi={editTarget}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateKPI(id, input);
        }}
        isSubmitting={isMutating}
        outcomes={outcomes}
        owners={owners}
        outcomesLoading={outcomesLoading}
        ownersLoading={ownersLoading}
      />

      <DeleteKPIDialog
        open={deleteTarget !== null}
        kpi={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={async (id) => {
          await deleteKPI(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
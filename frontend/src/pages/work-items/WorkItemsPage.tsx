import { Plus } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  CreateWorkItemDialog,
  DeleteWorkItemDialog,
  EditWorkItemDialog,
  WorkItemFilters,
  WorkItemsErrorState,
  WorkItemsLoadingState,
  WorkItemsPagination,
  WorkItemsTable,
  useAssigneeOptions,
  useSprintOptions,
  useWorkItems,
  type WorkItem,
  type WorkItemPriority,
  type WorkItemStatus,
  type WorkItemType,
} from "@/features/work-items";

const PAGE_SIZE = 20;

export default function WorkItemsPage() {
  const {
    data,
    items,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    filters,
    setProjectId,
    setSprintId,
    setAssigneeId,
    setItemTypes,
    setStatuses,
    setPriorities,
    setSearch,
    setPage,
    resetFilters,
    refresh,
    createWorkItem,
    updateWorkItem,
    deleteWorkItem,
  } = useWorkItems({ limit: PAGE_SIZE });

  const {
    projects,
    sprints,
    isLoadingProjects,
    isLoadingSprints,
  } = useSprintOptions(filters.projectId);
  const { assignees, isLoading: isLoadingAssignees } = useAssigneeOptions();

  const [isCreateOpen, setCreateOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<WorkItem | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<WorkItem | null>(null);

  const handleItemType = (value: WorkItemType | "") => {
    setItemTypes(value ? [value] : []);
  };
  const handleStatus = (value: WorkItemStatus | "") => {
    setStatuses(value ? [value] : []);
  };
  const handlePriority = (value: WorkItemPriority | "") => {
    setPriorities(value ? [value] : []);
  };

  const totalCount = data?.total ?? 0;
  const hasResults = items.length > 0;

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Work items</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Track stories, tasks, bugs, spikes, and epics across your projects.
          </p>
        </div>
        <Button type="button" onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4" />
          New work item
        </Button>
      </header>

      <WorkItemFilters
        projects={projects}
        sprints={sprints}
        assignees={assignees}
        isLoadingProjects={isLoadingProjects}
        isLoadingSprints={isLoadingSprints}
        isLoadingAssignees={isLoadingAssignees}
        projectId={filters.projectId}
        sprintId={filters.sprintId}
        assigneeId={filters.assigneeId}
        itemTypes={filters.itemTypes}
        statuses={filters.statuses}
        priorities={filters.priorities}
        search={filters.search}
        onProjectChange={setProjectId}
        onSprintChange={setSprintId}
        onAssigneeChange={setAssigneeId}
        onItemTypeChange={handleItemType}
        onStatusChange={handleStatus}
        onPriorityChange={handlePriority}
        onSearchChange={setSearch}
        onReset={resetFilters}
      />

      {isLoading && !data ? (
        <WorkItemsLoadingState />
      ) : error ? (
        <WorkItemsErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            filters.search ||
            filters.projectId ||
            filters.sprintId ||
            filters.assigneeId ||
            filters.itemTypes.length > 0 ||
            filters.statuses.length > 0 ||
            filters.priorities.length > 0
              ? "No work items match your filters"
              : "No work items yet"
          }
          description={
            filters.search
              ? "Try broadening the search or clearing filters."
              : "Create the first work item to begin tracking delivery."
          }
          action={
            <div className="flex items-center gap-2">
              <Button
                type="button"
                variant="outline"
                onClick={resetFilters}
              >
                Reset filters
              </Button>
              <Button type="button" onClick={() => setCreateOpen(true)}>
                <Plus className="h-4 w-4" />
                New work item
              </Button>
            </div>
          }
        />
      ) : (
        <div className="space-y-4">
          <WorkItemsTable
            items={items}
            sprints={sprints}
            assignees={assignees}
            isMutating={isMutating}
            onEdit={setEditTarget}
            onDelete={setDeleteTarget}
          />
          <WorkItemsPagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <CreateWorkItemDialog
        open={isCreateOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={async (input) => {
          await createWorkItem(input);
        }}
        isSubmitting={isMutating}
        defaultProjectId={filters.projectId}
      />

      <EditWorkItemDialog
        open={editTarget !== null}
        workItem={editTarget}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateWorkItem(id, input);
        }}
        isSubmitting={isMutating}
      />

      <DeleteWorkItemDialog
        open={deleteTarget !== null}
        workItem={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={async (id) => {
          await deleteWorkItem(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
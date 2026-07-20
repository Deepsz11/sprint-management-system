import { Plus } from "lucide-react";
import { useState } from "react";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  CompleteSprintDialog,
  CreateSprintDialog,
  DeleteSprintDialog,
  EditSprintDialog,
  Pagination,
  SprintFilters,
  SprintsErrorState,
  SprintsLoadingState,
  SprintsTable,
  useSprintProjects,
  useSprints,
  type Sprint,
} from "@/features/sprints";
import { useToast } from "@/providers/ToastProvider";

const PAGE_SIZE = 20;

export default function SprintsPage() {
  const {
    projects,
    isLoading: projectsLoading,
    error: projectsError,
  } = useSprintProjects();

  const {
    data,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    search,
    projectId,
    setSearch,
    setProjectId,
    setPage,
    refresh,
    createSprint,
    updateSprint,
    deleteSprint,
    startSprint,
    completeSprint,
  } = useSprints({ limit: PAGE_SIZE });

  const { toast } = useToast();

  const [isCreateOpen, setCreateOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<Sprint | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Sprint | null>(null);
  const [completeTarget, setCompleteTarget] = useState<Sprint | null>(null);

  const handleStart = async (sprint: Sprint) => {
    try {
      await startSprint(sprint.id);
      toast({ title: `${sprint.name} started`, variant: "success" });
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not start sprint",
        description: apiError.message,
        variant: "error",
      });
    }
  };

  const hasProjects = projects.length > 0;
  const hasResults = filtered.length > 0;
  const totalCount = data?.total ?? 0;
  const canCreate = hasProjects;

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Sprints</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Plan, run, and close sprints tied to your projects.
          </p>
        </div>
        <Button
          type="button"
          onClick={() => setCreateOpen(true)}
          disabled={!canCreate || projectsLoading}
        >
          <Plus className="h-4 w-4" />
          New sprint
        </Button>
      </header>

      <SprintFilters
        projects={projects}
        isLoadingProjects={projectsLoading}
        projectId={projectId}
        onProjectChange={setProjectId}
        search={search}
        onSearchChange={setSearch}
      />

      {projectsError ? (
        <SprintsErrorState
          message={projectsError.message}
          onRetry={() => window.location.reload()}
        />
      ) : !projectsLoading && !hasProjects ? (
        <EmptyState
          title="No projects available"
          description="Create a project first to start planning sprints."
        />
      ) : !projectId ? (
        <EmptyState
          title="Select a project"
          description="Pick a project above to view or create its sprints."
        />
      ) : isLoading && !data ? (
        <SprintsLoadingState />
      ) : error ? (
        <SprintsErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            search
              ? "No sprints match your search"
              : "No sprints in this project yet"
          }
          description={
            search
              ? "Try a different name, goal, or status — or clear the search."
              : "Create the first sprint to start tracking delivery."
          }
          action={
            search ? (
              <Button
                type="button"
                variant="outline"
                onClick={() => setSearch("")}
              >
                Clear search
              </Button>
            ) : (
              <Button type="button" onClick={() => setCreateOpen(true)}>
                <Plus className="h-4 w-4" />
                New sprint
              </Button>
            )
          }
        />
      ) : (
        <div className="space-y-4">
          <SprintsTable
            sprints={filtered}
            isMutating={isMutating}
            onEdit={setEditTarget}
            onDelete={setDeleteTarget}
            onStart={(sprint) => void handleStart(sprint)}
            onComplete={setCompleteTarget}
          />
          <Pagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <CreateSprintDialog
        open={isCreateOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={async (input) => {
          await createSprint(input);
        }}
        isSubmitting={isMutating}
        projects={projects}
        projectsLoading={projectsLoading}
        defaultProjectId={projectId}
      />

      <EditSprintDialog
        open={editTarget !== null}
        sprint={editTarget}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateSprint(id, input);
        }}
        isSubmitting={isMutating}
      />

      <CompleteSprintDialog
        open={completeTarget !== null}
        sprint={completeTarget}
        onClose={() => setCompleteTarget(null)}
        onSubmit={async (id, input) => {
          await completeSprint(id, input);
        }}
        isSubmitting={isMutating}
      />

      <DeleteSprintDialog
        open={deleteTarget !== null}
        sprint={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={async (id) => {
          await deleteSprint(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
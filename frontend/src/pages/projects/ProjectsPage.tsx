import { Plus } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import {
  CreateProjectDialog,
  DeleteProjectDialog,
  EditProjectDialog,
  Pagination,
  ProjectSearch,
  ProjectsErrorState,
  ProjectsLoadingState,
  ProjectsTable,
  useProjects,
  type Project,
} from "@/features/projects";
import { useToast } from "@/providers/ToastProvider";

const PAGE_SIZE = 20;

export default function ProjectsPage() {
  const {
    data,
    filtered,
    isLoading,
    isMutating,
    error,
    page,
    totalPages,
    search,
    includeArchived,
    setSearch,
    setIncludeArchived,
    setPage,
    refresh,
    createProject,
    updateProject,
    deleteProject,
  } = useProjects({ limit: PAGE_SIZE });
  const { toast } = useToast();

  const [isCreateOpen, setCreateOpen] = useState<boolean>(false);
  const [editTarget, setEditTarget] = useState<Project | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<Project | null>(null);

  const handleToggleArchive = async (project: Project) => {
    try {
      await updateProject(project.id, { is_archived: !project.is_archived });
      toast({
        title: project.is_archived
          ? "Project restored"
          : "Project archived",
        variant: "success",
      });
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "An unexpected error occurred";
      toast({
        title: "Could not update project",
        description: message,
        variant: "error",
      });
    }
  };

  const hasResults = filtered.length > 0;
  const totalCount = data?.total ?? 0;

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Projects</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage the projects that group sprints, work items, and outcomes.
          </p>
        </div>
        <Button type="button" onClick={() => setCreateOpen(true)}>
          <Plus className="h-4 w-4" />
          New project
        </Button>
      </header>

      <ProjectSearch
        value={search}
        onChange={setSearch}
        includeArchived={includeArchived}
        onIncludeArchivedChange={(value) => {
          setIncludeArchived(value);
          setPage(1);
        }}
      />

      {isLoading && !data ? (
        <ProjectsLoadingState />
      ) : error ? (
        <ProjectsErrorState
          message={error.message}
          onRetry={() => void refresh()}
        />
      ) : !hasResults ? (
        <EmptyState
          title={
            search
              ? "No projects match your search"
              : "No projects yet"
          }
          description={
            search
              ? "Try a different name, key, or slug — or clear the search."
              : "Create your first project to start tracking sprints and outcomes."
          }
          action={
            !search ? (
              <Button type="button" onClick={() => setCreateOpen(true)}>
                <Plus className="h-4 w-4" />
                New project
              </Button>
            ) : (
              <Button
                type="button"
                variant="outline"
                onClick={() => setSearch("")}
              >
                Clear search
              </Button>
            )
          }
        />
      ) : (
        <div className="space-y-4">
          <ProjectsTable
            projects={filtered}
            isMutating={isMutating}
            onEdit={setEditTarget}
            onDelete={setDeleteTarget}
            onToggleArchive={(project) => void handleToggleArchive(project)}
          />
          <Pagination
            page={page}
            totalPages={totalPages}
            total={totalCount}
            onChange={setPage}
          />
        </div>
      )}

      <CreateProjectDialog
        open={isCreateOpen}
        onClose={() => setCreateOpen(false)}
        onSubmit={async (input) => {
          await createProject(input);
        }}
        isSubmitting={isMutating}
      />

      <EditProjectDialog
        open={editTarget !== null}
        project={editTarget}
        onClose={() => setEditTarget(null)}
        onSubmit={async (id, input) => {
          await updateProject(id, input);
        }}
        isSubmitting={isMutating}
      />

      <DeleteProjectDialog
        open={deleteTarget !== null}
        project={deleteTarget}
        onClose={() => setDeleteTarget(null)}
        onConfirm={async (id) => {
          await deleteProject(id);
        }}
        isSubmitting={isMutating}
      />
    </div>
  );
}
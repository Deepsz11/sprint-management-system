import { Archive, ArchiveRestore, Pencil, Trash2 } from "lucide-react";

import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

import type { Project } from "../types";
import { ProjectStatusBadge } from "./ProjectStatusBadge";

interface ProjectsTableProps {
  readonly projects: Project[];
  readonly onEdit: (project: Project) => void;
  readonly onDelete: (project: Project) => void;
  readonly onToggleArchive: (project: Project) => void;
  readonly isMutating: boolean;
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

export function ProjectsTable({
  projects,
  onEdit,
  onDelete,
  onToggleArchive,
  isMutating,
}: ProjectsTableProps) {
  return (
    <div className="overflow-hidden rounded-lg border border-border bg-card">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-border text-sm">
          <thead className="bg-muted/50 text-left text-xs uppercase tracking-wide text-muted-foreground">
            <tr>
              <th scope="col" className="px-4 py-3 font-semibold">
                Key
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Name
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Status
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Start
              </th>
              <th scope="col" className="px-4 py-3 font-semibold">
                Target End
              </th>
              <th scope="col" className="px-4 py-3 text-right font-semibold">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {projects.map((project) => (
              <tr
                key={project.id}
                className={cn(
                  "transition-colors hover:bg-muted/30",
                  project.is_archived && "opacity-70",
                )}
              >
                <td className="px-4 py-3 font-mono text-xs font-semibold text-foreground">
                  {project.key}
                </td>
                <td className="px-4 py-3">
                  <div className="flex flex-col">
                    <span className="font-medium text-foreground">
                      {project.name}
                    </span>
                    {project.description && (
                      <span className="line-clamp-1 text-xs text-muted-foreground">
                        {project.description}
                      </span>
                    )}
                  </div>
                </td>
                <td className="px-4 py-3">
                  <ProjectStatusBadge isArchived={project.is_archived} />
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {formatDate(project.start_date)}
                </td>
                <td className="px-4 py-3 text-muted-foreground">
                  {formatDate(project.target_end_date)}
                </td>
                <td className="px-4 py-3">
                  <div className="flex items-center justify-end gap-1">
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={`Edit ${project.name}`}
                      onClick={() => onEdit(project)}
                      disabled={isMutating}
                    >
                      <Pencil className="h-4 w-4" />
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={
                        project.is_archived
                          ? `Restore ${project.name}`
                          : `Archive ${project.name}`
                      }
                      onClick={() => onToggleArchive(project)}
                      disabled={isMutating}
                    >
                      {project.is_archived ? (
                        <ArchiveRestore className="h-4 w-4" />
                      ) : (
                        <Archive className="h-4 w-4" />
                      )}
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      aria-label={`Delete ${project.name}`}
                      onClick={() => onDelete(project)}
                      disabled={isMutating}
                      className="text-destructive hover:bg-destructive/10 hover:text-destructive"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
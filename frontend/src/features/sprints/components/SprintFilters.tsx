import { Search } from "lucide-react";

import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";

import type { SprintProjectOption } from "../types";

interface SprintFiltersProps {
  readonly projects: SprintProjectOption[];
  readonly isLoadingProjects: boolean;
  readonly projectId: string | null;
  readonly onProjectChange: (id: string | null) => void;
  readonly search: string;
  readonly onSearchChange: (value: string) => void;
}

export function SprintFilters({
  projects,
  isLoadingProjects,
  projectId,
  onProjectChange,
  search,
  onSearchChange,
}: SprintFiltersProps) {
  return (
    <div className="flex flex-col gap-4 rounded-lg border border-border bg-card p-4 md:flex-row md:items-end md:justify-between">
      <div className="flex flex-1 flex-col gap-2 md:max-w-xs">
        <Label htmlFor="sprint-project">Project</Label>
        <select
          id="sprint-project"
          value={projectId ?? ""}
          onChange={(event) =>
            onProjectChange(event.target.value ? event.target.value : null)
          }
          className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          disabled={isLoadingProjects}
        >
          <option value="">
            {isLoadingProjects ? "Loading projects…" : "Select a project"}
          </option>
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name} ({project.key})
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-1 flex-col gap-2 md:max-w-sm">
        <Label htmlFor="sprint-search">Search</Label>
        <div className="relative">
          <Search
            aria-hidden="true"
            className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
          />
          <Input
            id="sprint-search"
            type="search"
            placeholder="Name, goal, or status…"
            value={search}
            onChange={(event) => onSearchChange(event.target.value)}
            className="pl-9"
            disabled={!projectId}
          />
        </div>
      </div>
    </div>
  );
}
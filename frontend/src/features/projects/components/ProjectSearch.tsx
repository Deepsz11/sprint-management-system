import { Search } from "lucide-react";

import { Input } from "@/components/ui/Input";

interface ProjectSearchProps {
  readonly value: string;
  readonly onChange: (value: string) => void;
  readonly includeArchived: boolean;
  readonly onIncludeArchivedChange: (value: boolean) => void;
}

export function ProjectSearch({
  value,
  onChange,
  includeArchived,
  onIncludeArchivedChange,
}: ProjectSearchProps) {
  return (
    <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="relative w-full sm:max-w-sm">
        <Search
          aria-hidden="true"
          className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground"
        />
        <Input
          type="search"
          placeholder="Search by name, key, slug…"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          className="pl-9"
          aria-label="Search projects"
        />
      </div>

      <label className="inline-flex items-center gap-2 text-sm text-muted-foreground">
        <input
          type="checkbox"
          checked={includeArchived}
          onChange={(event) => onIncludeArchivedChange(event.target.checked)}
          className="h-4 w-4 rounded border-input text-primary focus:ring-2 focus:ring-ring"
        />
        Include archived
      </label>
    </div>
  );
}
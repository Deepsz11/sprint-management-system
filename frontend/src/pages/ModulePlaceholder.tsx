import { Sparkles } from "lucide-react";

import { EmptyState } from "@/components/ui/EmptyState";

interface ModulePlaceholderProps {
  readonly title: string;
  readonly description?: string;
}

export default function ModulePlaceholder({
  title,
  description,
}: ModulePlaceholderProps) {
  return (
    <div className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          This module is part of the Sprint Business Outcome Tracer roadmap.
        </p>
      </header>

      <EmptyState
        title={`${title} is coming soon`}
        description={
          description ??
          "The foundation is in place. Feature screens for this module will be enabled in an upcoming release."
        }
        action={
          <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
            <Sparkles className="h-4 w-4 text-primary" />
            <span>Under active development</span>
          </div>
        }
      />
    </div>
  );
}
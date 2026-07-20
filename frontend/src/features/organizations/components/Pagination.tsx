import { ChevronLeft, ChevronRight } from "lucide-react";

import { Button } from "@/components/ui/Button";

interface PaginationProps {
  readonly page: number;
  readonly totalPages: number;
  readonly total: number;
  readonly onChange: (page: number) => void;
}

export function Pagination({
  page,
  totalPages,
  total,
  onChange,
}: PaginationProps) {
  const canPrev = page > 1;
  const canNext = page < totalPages;

  return (
    <div className="flex flex-col items-center justify-between gap-3 border-t border-border pt-4 text-sm text-muted-foreground sm:flex-row">
      <p>
        Page <span className="font-medium text-foreground">{page}</span> of{" "}
        <span className="font-medium text-foreground">{totalPages}</span>
        <span className="mx-2 opacity-50">•</span>
        <span>{total} total</span>
      </p>
      <div className="flex items-center gap-2">
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => onChange(page - 1)}
          disabled={!canPrev}
        >
          <ChevronLeft className="h-4 w-4" />
          Previous
        </Button>
        <Button
          type="button"
          variant="outline"
          size="sm"
          onClick={() => onChange(page + 1)}
          disabled={!canNext}
        >
          Next
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
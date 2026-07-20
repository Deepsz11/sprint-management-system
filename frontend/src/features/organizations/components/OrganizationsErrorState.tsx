import { AlertCircle } from "lucide-react";

import { Button } from "@/components/ui/Button";

interface OrganizationsErrorStateProps {
  readonly message: string;
  readonly onRetry: () => void;
}

export function OrganizationsErrorState({
  message,
  onRetry,
}: OrganizationsErrorStateProps) {
  return (
    <div
      role="alert"
      className="flex flex-col items-center justify-center gap-3 rounded-lg border border-destructive/40 bg-destructive/10 p-8 text-center text-destructive"
    >
      <AlertCircle className="h-6 w-6" aria-hidden="true" />
      <div>
        <h3 className="text-base font-semibold">
          Failed to load organizations
        </h3>
        <p className="mt-1 text-sm opacity-90">{message}</p>
      </div>
      <Button
        type="button"
        variant="outline"
        onClick={onRetry}
        className="border-destructive/40 text-destructive hover:bg-destructive/20"
      >
        Try again
      </Button>
    </div>
  );
}
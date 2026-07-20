import { Loader2, TriangleAlert } from "lucide-react";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { useToast } from "@/providers/ToastProvider";

import type { WorkItem } from "../types";
import { Modal } from "./Modal";

interface DeleteWorkItemDialogProps {
  readonly open: boolean;
  readonly workItem: WorkItem | null;
  readonly onClose: () => void;
  readonly onConfirm: (id: string) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function DeleteWorkItemDialog({
  open,
  workItem,
  onClose,
  onConfirm,
  isSubmitting,
}: DeleteWorkItemDialogProps) {
  const { toast } = useToast();

  const handleConfirm = async () => {
    if (!workItem) return;
    try {
      await onConfirm(workItem.id);
      toast({ title: "Work item deleted", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not delete work item",
        description: apiError.message,
        variant: "error",
      });
    }
  };

  return (
    <Modal
      open={open && workItem !== null}
      onClose={onClose}
      title="Delete work item"
      maxWidthClassName="max-w-md"
    >
      <div className="space-y-4">
        <div className="flex items-start gap-3 rounded-md border border-destructive/40 bg-destructive/10 p-3 text-destructive">
          <TriangleAlert className="mt-0.5 h-5 w-5" aria-hidden="true" />
          <div className="text-sm">
            <p className="font-medium">This action cannot be undone.</p>
            <p className="mt-1 opacity-90">
              {workItem ? (
                <>
                  You are about to permanently remove{" "}
                  <span className="font-semibold">{workItem.title}</span>.
                </>
              ) : (
                "Work item details are unavailable."
              )}
            </p>
          </div>
        </div>

        <div className="flex items-center justify-end gap-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={isSubmitting}
          >
            Cancel
          </Button>
          <Button
            type="button"
            variant="destructive"
            onClick={() => void handleConfirm()}
            disabled={isSubmitting || !workItem}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Deleting…
              </>
            ) : (
              "Delete work item"
            )}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
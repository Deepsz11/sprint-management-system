import { Loader2, ShieldAlert } from "lucide-react";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { useToast } from "@/providers/ToastProvider";

import type { User } from "../types";
import { Modal } from "./Modal";

interface DeactivateUserDialogProps {
  readonly open: boolean;
  readonly user: User | null;
  readonly onClose: () => void;
  readonly onConfirm: (id: string) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function DeactivateUserDialog({
  open,
  user,
  onClose,
  onConfirm,
  isSubmitting,
}: DeactivateUserDialogProps) {
  const { toast } = useToast();

  const handleConfirm = async () => {
    if (!user) return;
    try {
      await onConfirm(user.id);
      toast({ title: "User deactivated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not deactivate user",
        description: apiError.message,
        variant: "error",
      });
    }
  };

  return (
    <Modal
      open={open && user !== null}
      onClose={onClose}
      title="Deactivate user"
      maxWidthClassName="max-w-md"
    >
      <div className="space-y-4">
        <div className="flex items-start gap-3 rounded-md border border-destructive/40 bg-destructive/10 p-3 text-destructive">
          <ShieldAlert className="mt-0.5 h-5 w-5" aria-hidden="true" />
          <div className="text-sm">
            <p className="font-medium">
              The user will lose access to the platform.
            </p>
            <p className="mt-1 opacity-90">
              {user ? (
                <>
                  You are about to deactivate{" "}
                  <span className="font-semibold">{user.full_name}</span> (
                  {user.email}). Existing data will be preserved and you can
                  reactivate the account later.
                </>
              ) : (
                "User details are unavailable."
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
            disabled={isSubmitting || !user}
          >
            {isSubmitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Deactivating…
              </>
            ) : (
              "Deactivate user"
            )}
          </Button>
        </div>
      </div>
    </Modal>
  );
}
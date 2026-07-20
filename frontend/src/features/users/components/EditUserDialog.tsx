import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import type {
  UpdateUserInput,
  User,
  UserTeamOption,
} from "../types";
import { editUserSchema, type EditUserFormValues } from "../userSchemas";
import { ROLE_LABELS, useRoleOptions } from "../useRoleOptions";
import { USER_STATUS_LABELS } from "./UserStatusBadge";
import { Modal } from "./Modal";

interface EditUserDialogProps {
  readonly open: boolean;
  readonly user: User | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: UpdateUserInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly teams: UserTeamOption[];
  readonly teamsLoading: boolean;
  readonly currentTeamId?: string | null;
  readonly onTeamChange?: (userId: string, teamId: string | null) => void;
}

export function EditUserDialog({
  open,
  user,
  onClose,
  onSubmit,
  isSubmitting,
  teams,
  teamsLoading,
  currentTeamId,
  onTeamChange,
}: EditUserDialogProps) {
  const { toast } = useToast();
  const roleOptions = useRoleOptions();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditUserFormValues>({
    resolver: zodResolver(editUserSchema),
    defaultValues: {
      full_name: "",
      role: "viewer",
      status: "active",
      team_id: "",
    },
  });

  useEffect(() => {
    if (open && user) {
      reset({
        full_name: user.full_name,
        role: user.role,
        status: user.status,
        team_id: currentTeamId ?? "",
      });
    }
  }, [open, user, currentTeamId, reset]);

  const eligibleTeams = user?.organization_id
    ? teams.filter((team) => team.organization_id === user.organization_id)
    : teams;

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!user) return;
    try {
      const input: UpdateUserInput = {
        full_name: values.full_name.trim(),
        role: values.role,
        status: values.status,
      };
      await onSubmit(user.id, input);
      onTeamChange?.(user.id, values.team_id ? values.team_id : null);
      toast({ title: "User updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update user",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && user !== null}
      onClose={onClose}
      title={`Edit ${user?.full_name ?? "user"}`}
      description={user?.email}
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="user-edit-name">Full name</Label>
          <Input
            id="user-edit-name"
            {...register("full_name")}
            aria-invalid={Boolean(errors.full_name)}
          />
          {errors.full_name && (
            <p className="text-xs text-destructive">
              {errors.full_name.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <Label htmlFor="user-edit-role">Role</Label>
            <select
              id="user-edit-role"
              {...register("role")}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {roleOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {ROLE_LABELS[option.value]}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="user-edit-status">Status</Label>
            <select
              id="user-edit-status"
              {...register("status")}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              {(
                ["active", "invited", "suspended", "deactivated"] as const
              ).map((value) => (
                <option key={value} value={value}>
                  {USER_STATUS_LABELS[value]}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="user-edit-team">Team</Label>
            <select
              id="user-edit-team"
              {...register("team_id")}
              disabled={teamsLoading || eligibleTeams.length === 0}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <option value="">
                {teamsLoading
                  ? "Loading…"
                  : eligibleTeams.length === 0
                  ? "No teams available"
                  : "No team"}
              </option>
              {eligibleTeams.map((team) => (
                <option key={team.id} value={team.id}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="flex items-center justify-end gap-2 pt-2">
          <Button
            type="button"
            variant="ghost"
            onClick={onClose}
            disabled={submitting}
          >
            Cancel
          </Button>
          <Button type="submit" disabled={submitting || !isDirty}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Saving…
              </>
            ) : (
              "Save changes"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
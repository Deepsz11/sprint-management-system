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
  InviteUserInput,
  UserOrganizationOption,
  UserTeamOption,
} from "../types";
import {
  inviteUserSchema,
  type InviteUserFormValues,
} from "../userSchemas";
import { ROLE_LABELS, useRoleOptions } from "../useRoleOptions";
import { Modal } from "./Modal";

interface InviteUserDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: InviteUserInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly organizations: UserOrganizationOption[];
  readonly teams: UserTeamOption[];
  readonly orgsLoading: boolean;
  readonly teamsLoading: boolean;
  readonly defaultOrganizationId: string | null;
  readonly onTeamAssign?: (userId: string, teamId: string | null) => void;
}

export function InviteUserDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
  organizations,
  teams,
  orgsLoading,
  teamsLoading,
  defaultOrganizationId,
  onTeamAssign,
}: InviteUserDialogProps) {
  const { toast } = useToast();
  const roleOptions = useRoleOptions();

  const {
    register,
    handleSubmit,
    reset,
    watch,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<InviteUserFormValues>({
    resolver: zodResolver(inviteUserSchema),
    defaultValues: {
      email: "",
      full_name: "",
      password: "",
      role: "viewer",
      organization_id: defaultOrganizationId ?? "",
      team_id: "",
    },
  });

  useEffect(() => {
    if (!open) return;
    reset({
      email: "",
      full_name: "",
      password: "",
      role: "viewer",
      organization_id: defaultOrganizationId ?? "",
      team_id: "",
    });
  }, [open, defaultOrganizationId, reset]);

  const watchedOrg = watch("organization_id");
  const eligibleTeams = watchedOrg
    ? teams.filter((team) => team.organization_id === watchedOrg)
    : teams;

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    try {
      const input: InviteUserInput = {
        email: values.email.trim().toLowerCase(),
        full_name: values.full_name.trim(),
        password: values.password,
        role: values.role,
        organization_id: values.organization_id ? values.organization_id : null,
      };
      await onSubmit(input);
      if (values.team_id) {
        onTeamAssign?.(values.email.trim().toLowerCase(), values.team_id);
      }
      toast({ title: "Invitation sent", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not invite user",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Invite user"
      description="Add a new member to an organization."
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="user-invite-name">Full name</Label>
            <Input
              id="user-invite-name"
              placeholder="Jane Doe"
              autoComplete="off"
              {...register("full_name")}
              aria-invalid={Boolean(errors.full_name)}
            />
            {errors.full_name && (
              <p className="text-xs text-destructive">
                {errors.full_name.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="user-invite-email">Email</Label>
            <Input
              id="user-invite-email"
              type="email"
              placeholder="jane@acme.com"
              autoComplete="off"
              {...register("email")}
              aria-invalid={Boolean(errors.email)}
            />
            {errors.email && (
              <p className="text-xs text-destructive">{errors.email.message}</p>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="user-invite-password">Temporary password</Label>
          <Input
            id="user-invite-password"
            type="password"
            autoComplete="new-password"
            placeholder="Minimum 8 characters"
            {...register("password")}
            aria-invalid={Boolean(errors.password)}
          />
          {errors.password && (
            <p className="text-xs text-destructive">
              {errors.password.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <div className="space-y-2">
            <Label htmlFor="user-invite-role">Role</Label>
            <select
              id="user-invite-role"
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
            <Label htmlFor="user-invite-org">Organization</Label>
            <select
              id="user-invite-org"
              {...register("organization_id")}
              disabled={orgsLoading}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <option value="">
                {orgsLoading ? "Loading…" : "No organization"}
              </option>
              {organizations.map((organization) => (
                <option key={organization.id} value={organization.id}>
                  {organization.name}
                </option>
              ))}
            </select>
          </div>
          <div className="space-y-2">
            <Label htmlFor="user-invite-team">Team</Label>
            <select
              id="user-invite-team"
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
          <Button type="submit" disabled={submitting}>
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Inviting…
              </>
            ) : (
              "Send invitation"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
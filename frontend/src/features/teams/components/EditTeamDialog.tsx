import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import {
  editTeamSchema,
  emptyToNull,
  type EditTeamFormValues,
} from "../teamSchemas";
import type { Team, TeamLeadOption, UpdateTeamInput } from "../types";
import { Modal } from "./Modal";

interface EditTeamDialogProps {
  readonly open: boolean;
  readonly team: Team | null;
  readonly onClose: () => void;
  readonly onSubmit: (id: string, input: UpdateTeamInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly leads: TeamLeadOption[];
  readonly leadsLoading: boolean;
  readonly currentLeadId?: string | null;
  readonly currentIsActive?: boolean;
  readonly onLeadChange?: (teamId: string, leadId: string | null) => void;
  readonly onActiveChange?: (teamId: string, isActive: boolean) => void;
}

export function EditTeamDialog({
  open,
  team,
  onClose,
  onSubmit,
  isSubmitting,
  leads,
  leadsLoading,
  currentLeadId,
  currentIsActive = true,
  onLeadChange,
  onActiveChange,
}: EditTeamDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditTeamFormValues>({
    resolver: zodResolver(editTeamSchema),
    defaultValues: {
      name: "",
      description: "",
      team_lead_id: "",
      is_active: true,
    },
  });

  useEffect(() => {
    if (open && team) {
      reset({
        name: team.name,
        description: team.description ?? "",
        team_lead_id: currentLeadId ?? "",
        is_active: currentIsActive,
      });
    }
  }, [open, team, currentLeadId, currentIsActive, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!team) return;
    try {
      const input: UpdateTeamInput = {
        name: values.name.trim(),
        description: emptyToNull(values.description),
      };
      await onSubmit(team.id, input);
      onLeadChange?.(team.id, values.team_lead_id ? values.team_lead_id : null);
      onActiveChange?.(team.id, values.is_active);
      toast({ title: "Team updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update team",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && team !== null}
      onClose={onClose}
      title={`Edit ${team?.name ?? "team"}`}
      description={team ? `Slug: ${team.slug}` : undefined}
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="team-edit-name">Name</Label>
          <Input
            id="team-edit-name"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="team-edit-description">Description</Label>
          <textarea
            id="team-edit-description"
            rows={3}
            {...register("description")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="team-edit-lead">Team lead</Label>
          <select
            id="team-edit-lead"
            {...register("team_lead_id")}
            disabled={leadsLoading}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            <option value="">
              {leadsLoading ? "Loading…" : "Unassigned"}
            </option>
            {leads.map((lead) => (
              <option key={lead.id} value={lead.id}>
                {lead.full_name}
              </option>
            ))}
          </select>
        </div>

        <label className="inline-flex items-center gap-2 text-sm">
          <input
            type="checkbox"
            className="h-4 w-4 rounded border-input text-primary focus:ring-2 focus:ring-ring"
            {...register("is_active")}
          />
          Active
        </label>

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
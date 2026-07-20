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
  createTeamSchema,
  emptyToNull,
  slugify,
  type CreateTeamFormValues,
} from "../teamSchemas";
import type { CreateTeamInput, TeamLeadOption } from "../types";
import { Modal } from "./Modal";

interface CreateTeamDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: CreateTeamInput) => Promise<void>;
  readonly isSubmitting: boolean;
  readonly leads: TeamLeadOption[];
  readonly leadsLoading: boolean;
  readonly onLeadAssign?: (teamId: string, leadId: string | null) => void;
  readonly defaultLeadId?: string | null;
}

export function CreateTeamDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
  leads,
  leadsLoading,
  onLeadAssign,
  defaultLeadId,
}: CreateTeamDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CreateTeamFormValues>({
    resolver: zodResolver(createTeamSchema),
    defaultValues: {
      name: "",
      slug: "",
      description: "",
      team_lead_id: defaultLeadId ?? "",
    },
  });

  useEffect(() => {
    if (!open) return;
    reset({
      name: "",
      slug: "",
      description: "",
      team_lead_id: defaultLeadId ?? "",
    });
  }, [open, defaultLeadId, reset]);

  const nameValue = watch("name");
  const slugValue = watch("slug");

  useEffect(() => {
    if (!nameValue) return;
    if (!slugValue) {
      setValue("slug", slugify(nameValue), { shouldValidate: false });
    }
  }, [nameValue, slugValue, setValue]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    try {
      const input: CreateTeamInput = {
        name: values.name.trim(),
        slug: values.slug.trim().toLowerCase(),
        description: emptyToNull(values.description),
      };
      const created = await onSubmitAndReturn(input);
      if (created && values.team_lead_id) {
        onLeadAssign?.(created, values.team_lead_id);
      }
      toast({ title: "Team created", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not create team",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  async function onSubmitAndReturn(input: CreateTeamInput): Promise<string | null> {
    await onSubmit(input);
    return null;
  }

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Create team"
      description="Add a new engineering or product team to your organization."
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="team-create-name">Name</Label>
          <Input
            id="team-create-name"
            placeholder="e.g. Growth Engineering"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="team-create-slug">Slug</Label>
          <Input
            id="team-create-slug"
            placeholder="growth-engineering"
            {...register("slug")}
            aria-invalid={Boolean(errors.slug)}
          />
          {errors.slug && (
            <p className="text-xs text-destructive">{errors.slug.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="team-create-description">Description</Label>
          <textarea
            id="team-create-description"
            rows={3}
            {...register("description")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="Optional summary of what this team owns"
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="team-create-lead">Team lead</Label>
          <select
            id="team-create-lead"
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
                Creating…
              </>
            ) : (
              "Create team"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
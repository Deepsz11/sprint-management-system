import { zodResolver } from "@hookform/resolvers/zod";
import { Loader2 } from "lucide-react";
import { useEffect } from "react";
import { useForm } from "react-hook-form";

import { toApiError } from "@/api/errors";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import { useToast } from "@/providers/ToastProvider";

import { useTeams } from "../useTeams";
import {
  createProjectSchema,
  type CreateProjectFormValues,
} from "../projectSchemas";
import type { CreateProjectInput } from "../types";
import { Modal } from "./Modal";

interface CreateProjectDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: CreateProjectInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

function slugify(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 64);
}

function keyify(value: string): string {
  return value
    .toUpperCase()
    .replace(/[^A-Z0-9]+/g, "")
    .slice(0, 12);
}

export function CreateProjectDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
}: CreateProjectDialogProps) {
  const { teams, isLoading: teamsLoading, error: teamsError } = useTeams();
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CreateProjectFormValues>({
    resolver: zodResolver(createProjectSchema),
    defaultValues: {
      team_id: "",
      name: "",
      key: "",
      slug: "",
      description: "",
      start_date: "",
      target_end_date: "",
    },
  });

  useEffect(() => {
    if (!open) reset();
  }, [open, reset]);

  const nameValue = watch("name");
  const keyValue = watch("key");
  const slugValue = watch("slug");

  useEffect(() => {
    if (!nameValue) return;
    if (!keyValue) {
      setValue("key", keyify(nameValue), { shouldValidate: false });
    }
    if (!slugValue) {
      setValue("slug", slugify(nameValue), { shouldValidate: false });
    }
  }, [nameValue, keyValue, slugValue, setValue]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    try {
      const input: CreateProjectInput = {
        team_id: values.team_id,
        name: values.name.trim(),
        key: values.key.trim().toUpperCase(),
        slug: values.slug.trim().toLowerCase(),
        description: values.description ? values.description.trim() : null,
        start_date: values.start_date ? values.start_date : null,
        target_end_date: values.target_end_date ? values.target_end_date : null,
      };
      await onSubmit(input);
      toast({ title: "Project created", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not create project",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Create project"
      description="Projects group sprints, work items, and outcomes."
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="team_id">Team</Label>
          {teamsError && (
            <p className="text-xs text-destructive">{teamsError.message}</p>
          )}
          <select
            id="team_id"
            {...register("team_id")}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            disabled={teamsLoading}
            aria-invalid={Boolean(errors.team_id)}
          >
            <option value="">
              {teamsLoading ? "Loading teams…" : "Select a team"}
            </option>
            {teams.map((team) => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>
          {errors.team_id && (
            <p className="text-xs text-destructive">{errors.team_id.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="name">Name</Label>
          <Input
            id="name"
            placeholder="e.g. Sprint Outcome Tracer"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="key">Key</Label>
            <Input
              id="key"
              placeholder="SBOT"
              {...register("key")}
              aria-invalid={Boolean(errors.key)}
            />
            {errors.key && (
              <p className="text-xs text-destructive">{errors.key.message}</p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="slug">Slug</Label>
            <Input
              id="slug"
              placeholder="sprint-outcome-tracer"
              {...register("slug")}
              aria-invalid={Boolean(errors.slug)}
            />
            {errors.slug && (
              <p className="text-xs text-destructive">{errors.slug.message}</p>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <Label htmlFor="description">Description</Label>
          <textarea
            id="description"
            rows={3}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="Optional summary of what the project delivers"
            {...register("description")}
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <Label htmlFor="start_date">Start date</Label>
            <Input
              id="start_date"
              type="date"
              {...register("start_date")}
              aria-invalid={Boolean(errors.start_date)}
            />
            {errors.start_date && (
              <p className="text-xs text-destructive">
                {errors.start_date.message}
              </p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="target_end_date">Target end date</Label>
            <Input
              id="target_end_date"
              type="date"
              {...register("target_end_date")}
              aria-invalid={Boolean(errors.target_end_date)}
            />
            {errors.target_end_date && (
              <p className="text-xs text-destructive">
                {errors.target_end_date.message}
              </p>
            )}
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
                Creating…
              </>
            ) : (
              "Create project"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
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
  createOrganizationSchema,
  emptyToNull,
  slugify,
  type CreateOrganizationFormValues,
} from "../organizationSchemas";
import type { CreateOrganizationInput } from "../types";
import { Modal } from "./Modal";

interface CreateOrganizationDialogProps {
  readonly open: boolean;
  readonly onClose: () => void;
  readonly onSubmit: (input: CreateOrganizationInput) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function CreateOrganizationDialog({
  open,
  onClose,
  onSubmit,
  isSubmitting,
}: CreateOrganizationDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    watch,
    setValue,
    formState: { errors, isSubmitting: formSubmitting },
  } = useForm<CreateOrganizationFormValues>({
    resolver: zodResolver(createOrganizationSchema),
    defaultValues: {
      name: "",
      slug: "",
      description: "",
      billing_email: "",
    },
  });

  useEffect(() => {
    if (!open) return;
    reset({ name: "", slug: "", description: "", billing_email: "" });
  }, [open, reset]);

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
      const input: CreateOrganizationInput = {
        name: values.name.trim(),
        slug: values.slug.trim().toLowerCase(),
        description: emptyToNull(values.description),
        billing_email: emptyToNull(values.billing_email),
      };
      await onSubmit(input);
      toast({ title: "Organization created", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not create organization",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open}
      onClose={onClose}
      title="Create organization"
      description="Provision a new tenant in the system."
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="org-create-name">Name</Label>
          <Input
            id="org-create-name"
            placeholder="e.g. Acme Corporation"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="org-create-slug">Slug</Label>
          <Input
            id="org-create-slug"
            placeholder="acme"
            {...register("slug")}
            aria-invalid={Boolean(errors.slug)}
          />
          {errors.slug && (
            <p className="text-xs text-destructive">{errors.slug.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="org-create-description">Description</Label>
          <textarea
            id="org-create-description"
            rows={3}
            {...register("description")}
            className="flex w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="Optional summary shown to admins"
          />
          {errors.description && (
            <p className="text-xs text-destructive">
              {errors.description.message}
            </p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="org-create-billing-email">Billing email</Label>
          <Input
            id="org-create-billing-email"
            type="email"
            autoComplete="off"
            placeholder="billing@acme.com"
            {...register("billing_email")}
            aria-invalid={Boolean(errors.billing_email)}
          />
          {errors.billing_email && (
            <p className="text-xs text-destructive">
              {errors.billing_email.message}
            </p>
          )}
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
              "Create organization"
            )}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
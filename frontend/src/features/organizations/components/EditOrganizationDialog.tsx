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
  editOrganizationSchema,
  emptyToNull,
  type EditOrganizationFormValues,
} from "../organizationSchemas";
import type { Organization, UpdateOrganizationInput } from "../types";
import { Modal } from "./Modal";

interface EditOrganizationDialogProps {
  readonly open: boolean;
  readonly organization: Organization | null;
  readonly onClose: () => void;
  readonly onSubmit: (
    id: string,
    input: UpdateOrganizationInput,
  ) => Promise<void>;
  readonly isSubmitting: boolean;
}

export function EditOrganizationDialog({
  open,
  organization,
  onClose,
  onSubmit,
  isSubmitting,
}: EditOrganizationDialogProps) {
  const { toast } = useToast();

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting: formSubmitting, isDirty },
  } = useForm<EditOrganizationFormValues>({
    resolver: zodResolver(editOrganizationSchema),
    defaultValues: {
      name: "",
      description: "",
      billing_email: "",
      is_active: true,
    },
  });

  useEffect(() => {
    if (open && organization) {
      reset({
        name: organization.name,
        description: organization.description ?? "",
        billing_email: organization.billing_email ?? "",
        is_active: organization.is_active,
      });
    }
  }, [open, organization, reset]);

  const submitting = isSubmitting || formSubmitting;

  const submit = handleSubmit(async (values) => {
    if (!organization) return;
    try {
      const input: UpdateOrganizationInput = {
        name: values.name.trim(),
        description: emptyToNull(values.description),
        billing_email: emptyToNull(values.billing_email),
        is_active: values.is_active,
      };
      await onSubmit(organization.id, input);
      toast({ title: "Organization updated", variant: "success" });
      onClose();
    } catch (err) {
      const apiError = toApiError(err);
      toast({
        title: "Could not update organization",
        description: apiError.message,
        variant: "error",
      });
    }
  });

  return (
    <Modal
      open={open && organization !== null}
      onClose={onClose}
      title={`Edit ${organization?.name ?? "organization"}`}
      description={organization ? `Slug: ${organization.slug}` : undefined}
      maxWidthClassName="max-w-xl"
    >
      <form onSubmit={submit} className="space-y-4" noValidate>
        <div className="space-y-2">
          <Label htmlFor="org-edit-name">Name</Label>
          <Input
            id="org-edit-name"
            {...register("name")}
            aria-invalid={Boolean(errors.name)}
          />
          {errors.name && (
            <p className="text-xs text-destructive">{errors.name.message}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="org-edit-description">Description</Label>
          <textarea
            id="org-edit-description"
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
          <Label htmlFor="org-edit-billing-email">Billing email</Label>
          <Input
            id="org-edit-billing-email"
            type="email"
            autoComplete="off"
            {...register("billing_email")}
            aria-invalid={Boolean(errors.billing_email)}
          />
          {errors.billing_email && (
            <p className="text-xs text-destructive">
              {errors.billing_email.message}
            </p>
          )}
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
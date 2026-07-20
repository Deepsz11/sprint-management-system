import { z } from "zod";

const slugRegex = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const optionalDescription = z
  .string()
  .trim()
  .max(2000, "Description must be 2000 characters or fewer")
  .optional()
  .or(z.literal(""));

const optionalLead = z.string().uuid().optional().or(z.literal(""));

export const createTeamSchema = z.object({
  name: z
    .string()
    .trim()
    .min(1, "Name is required")
    .max(200, "Name must be 200 characters or fewer"),
  slug: z
    .string()
    .trim()
    .min(2, "Slug must be between 2 and 64 characters")
    .max(64, "Slug must be between 2 and 64 characters")
    .regex(slugRegex, "Use lowercase letters, digits, and hyphens only"),
  description: optionalDescription,
  team_lead_id: optionalLead,
});

export type CreateTeamFormValues = z.infer<typeof createTeamSchema>;

export const editTeamSchema = z.object({
  name: z
    .string()
    .trim()
    .min(1, "Name is required")
    .max(200, "Name must be 200 characters or fewer"),
  description: optionalDescription,
  team_lead_id: optionalLead,
  is_active: z.boolean(),
});

export type EditTeamFormValues = z.infer<typeof editTeamSchema>;

export function emptyToNull(value: string | undefined | null): string | null {
  if (value === undefined || value === null) return null;
  const trimmed = value.trim();
  return trimmed.length === 0 ? null : trimmed;
}

export function slugify(value: string): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 64);
}
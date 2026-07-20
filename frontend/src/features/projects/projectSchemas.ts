import { z } from "zod";

const slugRegex = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const keyRegex = /^[A-Z0-9]+$/;

const optionalDate = z
  .string()
  .trim()
  .regex(/^\d{4}-\d{2}-\d{2}$/, "Use YYYY-MM-DD")
  .optional()
  .or(z.literal(""));

export const createProjectSchema = z
  .object({
    team_id: z.string().uuid("Select a team"),
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(200, "Name must be 200 characters or fewer"),
    key: z
      .string()
      .trim()
      .min(2, "Key must be between 2 and 12 characters")
      .max(12, "Key must be between 2 and 12 characters")
      .regex(keyRegex, "Key must be uppercase alphanumeric")
      .transform((v) => v.toUpperCase()),
    slug: z
      .string()
      .trim()
      .min(2, "Slug must be between 2 and 64 characters")
      .max(64, "Slug must be between 2 and 64 characters")
      .regex(
        slugRegex,
        "Slug must be lowercase alphanumeric with hyphens",
      ),
    description: z
      .string()
      .trim()
      .max(2000, "Description must be 2000 characters or fewer")
      .optional()
      .or(z.literal("")),
    start_date: optionalDate,
    target_end_date: optionalDate,
  })
  .superRefine((values, ctx) => {
    if (values.start_date && values.target_end_date) {
      if (values.target_end_date < values.start_date) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Target end date cannot be before start date",
          path: ["target_end_date"],
        });
      }
    }
  });

export type CreateProjectFormValues = z.infer<typeof createProjectSchema>;

export const editProjectSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(200, "Name must be 200 characters or fewer"),
    description: z
      .string()
      .trim()
      .max(2000, "Description must be 2000 characters or fewer")
      .optional()
      .or(z.literal("")),
    start_date: optionalDate,
    target_end_date: optionalDate,
    is_archived: z.boolean(),
  })
  .superRefine((values, ctx) => {
    if (values.start_date && values.target_end_date) {
      if (values.target_end_date < values.start_date) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          message: "Target end date cannot be before start date",
          path: ["target_end_date"],
        });
      }
    }
  });

export type EditProjectFormValues = z.infer<typeof editProjectSchema>;
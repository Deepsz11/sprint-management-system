import { z } from "zod";

const STATUSES = [
  "proposed",
  "active",
  "achieved",
  "at_risk",
  "off_track",
  "abandoned",
] as const;

const decimalString = z
  .string()
  .trim()
  .regex(
    /^-?\d+(\.\d+)?$/,
    "Enter a number (up to 6 decimal places)",
  );

const optionalDecimal = z.union([z.literal(""), decimalString]).optional();

const percentString = z
  .string()
  .trim()
  .regex(/^-?\d+(\.\d+)?$/, "Enter a number")
  .refine((value) => {
    const parsed = Number(value);
    return parsed >= 0 && parsed <= 100;
  }, "Must be between 0 and 100");

const optionalPercent = z.union([z.literal(""), percentString]).optional();

const optionalDate = z
  .string()
  .trim()
  .regex(/^\d{4}-\d{2}-\d{2}$/, "Use YYYY-MM-DD")
  .optional()
  .or(z.literal(""));

const optionalOwner = z.string().uuid().optional().or(z.literal(""));

const optionalDescription = z
  .string()
  .trim()
  .max(4000, "Must be 4000 characters or fewer")
  .optional()
  .or(z.literal(""));

export const createBusinessOutcomeSchema = z.object({
  name: z
    .string()
    .trim()
    .min(1, "Name is required")
    .max(300, "Must be 300 characters or fewer"),
  description: optionalDescription,
  hypothesis: optionalDescription,
  owner_id: optionalOwner,
  target_date: optionalDate,
  baseline_value: optionalDecimal,
  target_value: optionalDecimal,
  current_value: optionalDecimal,
  confidence_score: optionalPercent,
  financial_impact_estimate: optionalDecimal,
});

export type CreateBusinessOutcomeFormValues = z.infer<
  typeof createBusinessOutcomeSchema
>;

export const editBusinessOutcomeSchema = z.object({
  name: z
    .string()
    .trim()
    .min(1, "Name is required")
    .max(300, "Must be 300 characters or fewer"),
  description: optionalDescription,
  hypothesis: optionalDescription,
  owner_id: optionalOwner,
  status: z.enum(STATUSES),
  target_date: optionalDate,
  baseline_value: optionalDecimal,
  target_value: optionalDecimal,
  current_value: optionalDecimal,
  confidence_score: optionalPercent,
  financial_impact_estimate: optionalDecimal,
});

export type EditBusinessOutcomeFormValues = z.infer<
  typeof editBusinessOutcomeSchema
>;

export const OUTCOME_STATUS_OPTIONS = STATUSES;

export function emptyToNull(value: string | undefined | null): string | null {
  if (value === undefined || value === null) return null;
  const trimmed = value.trim();
  return trimmed.length === 0 ? null : trimmed;
}
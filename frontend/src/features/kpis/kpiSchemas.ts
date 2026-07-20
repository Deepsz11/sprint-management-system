import { z } from "zod";

const UNITS = [
  "currency",
  "percent",
  "count",
  "ratio",
  "duration_seconds",
  "duration_days",
  "score",
] as const;

const DIRECTIONS = ["increase", "decrease", "maintain"] as const;

const decimalString = z
  .string()
  .trim()
  .regex(/^-?\d+(\.\d+)?$/, "Enter a number (up to 6 decimal places)");

const optionalDecimal = z.union([z.literal(""), decimalString]).optional();

const optionalCurrency = z
  .string()
  .trim()
  .regex(/^[A-Za-z]{3}$/, "Use a 3-letter currency code")
  .transform((v) => v.toUpperCase())
  .optional()
  .or(z.literal(""));

const optionalFrequency = z
  .union([
    z.literal(""),
    z.coerce
      .number({ invalid_type_error: "Enter a number" })
      .int("Must be a whole number")
      .min(1, "Must be at least 1")
      .max(8760, "Value is too large"),
  ])
  .optional();

const optionalDescription = z
  .string()
  .trim()
  .max(2000, "Must be 2000 characters or fewer")
  .optional()
  .or(z.literal(""));

const optionalDataSource = z
  .string()
  .trim()
  .max(500, "Must be 500 characters or fewer")
  .optional()
  .or(z.literal(""));

const optionalOutcome = z.string().uuid().optional().or(z.literal(""));
const optionalOwner = z.string().uuid().optional().or(z.literal(""));

export const createKPISchema = z
  .object({
    outcome_id: optionalOutcome,
    owner_id: optionalOwner,
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(200, "Must be 200 characters or fewer"),
    description: optionalDescription,
    unit: z.enum(UNITS),
    currency: optionalCurrency,
    direction: z.enum(DIRECTIONS),
    baseline_value: optionalDecimal,
    target_value: optionalDecimal,
    current_value: optionalDecimal,
    data_source: optionalDataSource,
    refresh_frequency_hours: optionalFrequency,
  })
  .superRefine((values, ctx) => {
    if (values.unit === "currency" && !values.currency) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Currency is required for currency-typed KPIs",
        path: ["currency"],
      });
    }
    if (values.unit !== "currency" && values.currency) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "Currency should only be set for currency-typed KPIs",
        path: ["currency"],
      });
    }
  });

export type CreateKPIFormValues = z.infer<typeof createKPISchema>;

export const editKPISchema = z.object({
  outcome_id: optionalOutcome,
  owner_id: optionalOwner,
  name: z
    .string()
    .trim()
    .min(1, "Name is required")
    .max(200, "Must be 200 characters or fewer"),
  description: optionalDescription,
  direction: z.enum(DIRECTIONS),
  baseline_value: optionalDecimal,
  target_value: optionalDecimal,
  current_value: optionalDecimal,
  data_source: optionalDataSource,
  refresh_frequency_hours: optionalFrequency,
  is_active: z.boolean(),
});

export type EditKPIFormValues = z.infer<typeof editKPISchema>;

export const KPI_UNIT_OPTIONS = UNITS;
export const KPI_DIRECTION_OPTIONS = DIRECTIONS;

export function emptyToNull(value: string | undefined | null): string | null {
  if (value === undefined || value === null) return null;
  const trimmed = value.trim();
  return trimmed.length === 0 ? null : trimmed;
}
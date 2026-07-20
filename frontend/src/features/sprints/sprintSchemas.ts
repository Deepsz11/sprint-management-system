import { z } from "zod";

const dateString = z
  .string()
  .trim()
  .regex(/^\d{4}-\d{2}-\d{2}$/, "Use YYYY-MM-DD");

const optionalGoal = z
  .string()
  .trim()
  .max(2000, "Goal must be 2000 characters or fewer")
  .optional()
  .or(z.literal(""));

export const createSprintSchema = z
  .object({
    project_id: z.string().uuid("Select a project"),
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(200, "Name must be 200 characters or fewer"),
    goal: optionalGoal,
    start_date: dateString,
    end_date: dateString,
    planned_capacity: z
      .coerce.number({ invalid_type_error: "Enter a number" })
      .int("Must be a whole number")
      .min(0, "Cannot be negative")
      .max(10000, "Value is too large"),
  })
  .superRefine((values, ctx) => {
    if (values.end_date < values.start_date) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "End date cannot be before start date",
        path: ["end_date"],
      });
    }
  });

export type CreateSprintFormValues = z.infer<typeof createSprintSchema>;

export const editSprintSchema = z
  .object({
    name: z
      .string()
      .trim()
      .min(1, "Name is required")
      .max(200, "Name must be 200 characters or fewer"),
    goal: optionalGoal,
    start_date: dateString,
    end_date: dateString,
    planned_capacity: z
      .coerce.number({ invalid_type_error: "Enter a number" })
      .int("Must be a whole number")
      .min(0, "Cannot be negative")
      .max(10000, "Value is too large"),
  })
  .superRefine((values, ctx) => {
    if (values.end_date < values.start_date) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: "End date cannot be before start date",
        path: ["end_date"],
      });
    }
  });

export type EditSprintFormValues = z.infer<typeof editSprintSchema>;

export const completeSprintSchema = z.object({
  completed_points: z
    .coerce.number({ invalid_type_error: "Enter a number" })
    .int("Must be a whole number")
    .min(0, "Cannot be negative")
    .max(100000, "Value is too large"),
});

export type CompleteSprintFormValues = z.infer<typeof completeSprintSchema>;
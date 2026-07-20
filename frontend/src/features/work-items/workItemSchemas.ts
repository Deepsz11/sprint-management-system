import { z } from "zod";

const ITEM_TYPES = ["epic", "story", "task", "bug", "spike"] as const;
const PRIORITIES = ["critical", "high", "medium", "low"] as const;
const STATUSES = [
  "backlog",
  "todo",
  "in_progress",
  "in_review",
  "done",
  "cancelled",
] as const;

const optionalDescription = z
  .string()
  .trim()
  .max(10000, "Description must be 10000 characters or fewer")
  .optional()
  .or(z.literal(""));

const optionalPoints = z
  .union([
    z.literal(""),
    z.coerce
      .number({ invalid_type_error: "Enter a number" })
      .int("Must be a whole number")
      .min(0, "Cannot be negative")
      .max(1000, "Value is too large"),
  ])
  .optional();

const optionalHours = z
  .union([
    z.literal(""),
    z.coerce
      .number({ invalid_type_error: "Enter a number" })
      .min(0, "Cannot be negative")
      .max(10000, "Value is too large"),
  ])
  .optional();

const optionalLabels = z
  .string()
  .trim()
  .max(2000, "Labels string is too long")
  .optional()
  .or(z.literal(""));

export const createWorkItemSchema = z.object({
  project_id: z.string().uuid("Select a project"),
  sprint_id: z.string().uuid().optional().or(z.literal("")),
  title: z
    .string()
    .trim()
    .min(1, "Title is required")
    .max(500, "Title must be 500 characters or fewer"),
  description: optionalDescription,
  item_type: z.enum(ITEM_TYPES),
  priority: z.enum(PRIORITIES),
  story_points: optionalPoints,
  estimated_hours: optionalHours,
  assignee_id: z.string().uuid().optional().or(z.literal("")),
  labels: optionalLabels,
});

export type CreateWorkItemFormValues = z.infer<typeof createWorkItemSchema>;

export const editWorkItemSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, "Title is required")
    .max(500, "Title must be 500 characters or fewer"),
  description: optionalDescription,
  status: z.enum(STATUSES),
  priority: z.enum(PRIORITIES),
  story_points: optionalPoints,
  estimated_hours: optionalHours,
  sprint_id: z.string().uuid().optional().or(z.literal("")),
  assignee_id: z.string().uuid().optional().or(z.literal("")),
  labels: optionalLabels,
});

export type EditWorkItemFormValues = z.infer<typeof editWorkItemSchema>;

export const ITEM_TYPE_OPTIONS = ITEM_TYPES;
export const PRIORITY_OPTIONS = PRIORITIES;
export const STATUS_OPTIONS = STATUSES;

export function parseLabels(raw: string | undefined | null): string[] {
  if (!raw) return [];
  return raw
    .split(",")
    .map((token) => token.trim().toLowerCase())
    .filter((token) => token.length > 0);
}

export function stringifyLabels(labels: string[] | undefined | null): string {
  if (!labels || labels.length === 0) return "";
  return labels.join(", ");
}
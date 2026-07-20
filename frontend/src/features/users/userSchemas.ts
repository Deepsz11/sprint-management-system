import { z } from "zod";

const ROLES = [
  "super_admin",
  "org_admin",
  "executive",
  "product_manager",
  "engineering_manager",
  "engineer",
  "viewer",
] as const;

const STATUSES = ["active", "invited", "suspended", "deactivated"] as const;

const optionalOrg = z.string().uuid().optional().or(z.literal(""));
const optionalTeam = z.string().uuid().optional().or(z.literal(""));

export const inviteUserSchema = z.object({
  email: z
    .string()
    .trim()
    .min(1, "Email is required")
    .email("Enter a valid email address"),
  full_name: z
    .string()
    .trim()
    .min(1, "Full name is required")
    .max(200, "Must be 200 characters or fewer"),
  password: z
    .string()
    .min(8, "Must be at least 8 characters")
    .max(128, "Must be 128 characters or fewer"),
  role: z.enum(ROLES),
  organization_id: optionalOrg,
  team_id: optionalTeam,
});

export type InviteUserFormValues = z.infer<typeof inviteUserSchema>;

export const editUserSchema = z.object({
  full_name: z
    .string()
    .trim()
    .min(1, "Full name is required")
    .max(200, "Must be 200 characters or fewer"),
  role: z.enum(ROLES),
  status: z.enum(STATUSES),
  team_id: optionalTeam,
});

export type EditUserFormValues = z.infer<typeof editUserSchema>;

export const USER_ROLE_OPTIONS = ROLES;
export const USER_STATUS_OPTIONS = STATUSES;
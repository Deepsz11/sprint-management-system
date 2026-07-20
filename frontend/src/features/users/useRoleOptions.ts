import type { UserRole } from "./types";
import { USER_ROLE_OPTIONS } from "./userSchemas";

export interface RoleOption {
  readonly value: UserRole;
  readonly label: string;
}

const LABELS: Record<UserRole, string> = {
  super_admin: "Super Admin",
  org_admin: "Org Admin",
  executive: "Executive",
  product_manager: "Product Manager",
  engineering_manager: "Engineering Manager",
  engineer: "Engineer",
  viewer: "Viewer",
};

export function useRoleOptions(): RoleOption[] {
  return USER_ROLE_OPTIONS.map((value) => ({
    value,
    label: LABELS[value],
  }));
}

export const ROLE_LABELS = LABELS;
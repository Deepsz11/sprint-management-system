export type UserRole =
  | "super_admin"
  | "org_admin"
  | "executive"
  | "product_manager"
  | "engineering_manager"
  | "engineer"
  | "viewer";

export type UserStatus =
  | "active"
  | "invited"
  | "suspended"
  | "deactivated";

export interface User {
  readonly id: string;
  readonly email: string;
  readonly full_name: string;
  readonly organization_id: string | null;
  readonly role: UserRole;
  readonly status: UserStatus;
  readonly last_login_at: string | null;
  readonly is_email_verified: boolean;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface UserOrganizationOption {
  readonly id: string;
  readonly name: string;
  readonly slug: string;
  readonly is_active: boolean;
}

export interface UserTeamOption {
  readonly id: string;
  readonly organization_id: string;
  readonly name: string;
  readonly slug: string;
}

export interface PaginatedUsers {
  readonly items: User[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedUserOrganizations {
  readonly items: UserOrganizationOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedUserTeams {
  readonly items: UserTeamOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface InviteUserInput {
  readonly email: string;
  readonly password: string;
  readonly full_name: string;
  readonly role: UserRole;
  readonly organization_id?: string | null;
}

export interface UpdateUserInput {
  readonly full_name?: string;
  readonly role?: UserRole;
  readonly status?: UserStatus;
}

export interface UserListParams {
  readonly limit: number;
  readonly offset: number;
  readonly role?: UserRole;
  readonly search?: string;
}
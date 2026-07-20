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

export interface AuthUser {
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

export interface TokenPair {
  readonly access_token: string;
  readonly refresh_token: string;
  readonly token_type: string;
  readonly expires_in: number;
}

export interface LoginCredentials {
  readonly email: string;
  readonly password: string;
}
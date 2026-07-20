export interface Organization {
  readonly id: string;
  readonly name: string;
  readonly slug: string;
  readonly description: string | null;
  readonly billing_email: string | null;
  readonly is_active: boolean;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface PaginatedOrganizations {
  readonly items: Organization[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface CreateOrganizationInput {
  readonly name: string;
  readonly slug: string;
  readonly description?: string | null;
  readonly billing_email?: string | null;
}

export interface UpdateOrganizationInput {
  readonly name?: string;
  readonly description?: string | null;
  readonly billing_email?: string | null;
  readonly is_active?: boolean;
}

export interface OrganizationListParams {
  readonly limit: number;
  readonly offset: number;
}
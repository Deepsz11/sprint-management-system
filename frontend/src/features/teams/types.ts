export interface Team {
  readonly id: string;
  readonly organization_id: string;
  readonly name: string;
  readonly slug: string;
  readonly description: string | null;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface TeamOrganizationOption {
  readonly id: string;
  readonly name: string;
  readonly slug: string;
  readonly is_active: boolean;
}

export interface TeamLeadOption {
  readonly id: string;
  readonly email: string;
  readonly full_name: string;
  readonly organization_id: string | null;
  readonly role: string;
  readonly status: string;
}

export interface PaginatedTeams {
  readonly items: Team[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedTeamOrganizations {
  readonly items: TeamOrganizationOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedTeamLeads {
  readonly items: TeamLeadOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface CreateTeamInput {
  readonly name: string;
  readonly slug: string;
  readonly description?: string | null;
}

export interface UpdateTeamInput {
  readonly name?: string;
  readonly description?: string | null;
}

export interface TeamListParams {
  readonly limit: number;
  readonly offset: number;
}
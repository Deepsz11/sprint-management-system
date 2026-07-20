export interface Project {
  readonly id: string;
  readonly organization_id: string;
  readonly team_id: string;
  readonly name: string;
  readonly key: string;
  readonly slug: string;
  readonly description: string | null;
  readonly start_date: string | null;
  readonly target_end_date: string | null;
  readonly is_archived: boolean;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface Team {
  readonly id: string;
  readonly organization_id: string;
  readonly name: string;
  readonly slug: string;
  readonly description: string | null;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface CreateProjectInput {
  readonly team_id: string;
  readonly name: string;
  readonly key: string;
  readonly slug: string;
  readonly description?: string | null;
  readonly start_date?: string | null;
  readonly target_end_date?: string | null;
}

export interface UpdateProjectInput {
  readonly name?: string;
  readonly description?: string | null;
  readonly start_date?: string | null;
  readonly target_end_date?: string | null;
  readonly is_archived?: boolean;
}

export interface PaginatedProjects {
  readonly items: Project[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedTeams {
  readonly items: Team[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface ProjectListParams {
  readonly limit: number;
  readonly offset: number;
  readonly team_id?: string;
  readonly include_archived?: boolean;
}
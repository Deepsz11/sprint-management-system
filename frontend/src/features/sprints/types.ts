export type SprintStatus =
  | "planned"
  | "active"
  | "completed"
  | "cancelled";

export interface Sprint {
  readonly id: string;
  readonly project_id: string;
  readonly name: string;
  readonly goal: string | null;
  readonly start_date: string;
  readonly end_date: string;
  readonly status: SprintStatus;
  readonly started_at: string | null;
  readonly completed_at: string | null;
  readonly planned_capacity: number;
  readonly completed_points: number;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface SprintProjectOption {
  readonly id: string;
  readonly organization_id: string;
  readonly team_id: string;
  readonly name: string;
  readonly key: string;
  readonly slug: string;
  readonly is_archived: boolean;
}

export interface PaginatedSprints {
  readonly items: Sprint[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedSprintProjects {
  readonly items: SprintProjectOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface CreateSprintInput {
  readonly project_id: string;
  readonly name: string;
  readonly goal?: string | null;
  readonly start_date: string;
  readonly end_date: string;
  readonly planned_capacity: number;
}

export interface UpdateSprintInput {
  readonly name?: string;
  readonly goal?: string | null;
  readonly start_date?: string;
  readonly end_date?: string;
  readonly planned_capacity?: number;
}

export interface CompleteSprintInput {
  readonly completed_points: number;
}

export interface SprintListParams {
  readonly project_id: string;
  readonly limit: number;
  readonly offset: number;
}
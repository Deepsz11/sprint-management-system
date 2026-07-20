export type OutcomeStatus =
  | "proposed"
  | "active"
  | "achieved"
  | "at_risk"
  | "off_track"
  | "abandoned";

export interface BusinessOutcome {
  readonly id: string;
  readonly organization_id: string;
  readonly owner_id: string | null;
  readonly name: string;
  readonly description: string | null;
  readonly hypothesis: string | null;
  readonly status: OutcomeStatus;
  readonly target_date: string | null;
  readonly baseline_value: string | number | null;
  readonly target_value: string | number | null;
  readonly current_value: string | number | null;
  readonly progress_percent: string | number;
  readonly confidence_score: string | number | null;
  readonly financial_impact_estimate: string | number | null;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface OutcomeProjectOption {
  readonly id: string;
  readonly organization_id: string;
  readonly team_id: string;
  readonly name: string;
  readonly key: string;
  readonly slug: string;
  readonly is_archived: boolean;
}

export interface OutcomeOwnerOption {
  readonly id: string;
  readonly email: string;
  readonly full_name: string;
  readonly organization_id: string | null;
  readonly role: string;
  readonly status: string;
}

export interface OutcomeKpiOption {
  readonly id: string;
  readonly organization_id: string;
  readonly outcome_id: string | null;
  readonly owner_id: string | null;
  readonly name: string;
  readonly unit: string;
  readonly currency: string | null;
  readonly direction: string;
  readonly is_active: boolean;
}

export interface PaginatedBusinessOutcomes {
  readonly items: BusinessOutcome[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedOutcomeProjects {
  readonly items: OutcomeProjectOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedOutcomeOwners {
  readonly items: OutcomeOwnerOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedOutcomeKpis {
  readonly items: OutcomeKpiOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface CreateBusinessOutcomeInput {
  readonly name: string;
  readonly description?: string | null;
  readonly hypothesis?: string | null;
  readonly owner_id?: string | null;
  readonly target_date?: string | null;
  readonly baseline_value?: string | null;
  readonly target_value?: string | null;
  readonly current_value?: string | null;
  readonly confidence_score?: string | null;
  readonly financial_impact_estimate?: string | null;
}

export interface UpdateBusinessOutcomeInput {
  readonly name?: string;
  readonly description?: string | null;
  readonly hypothesis?: string | null;
  readonly owner_id?: string | null;
  readonly status?: OutcomeStatus;
  readonly target_date?: string | null;
  readonly baseline_value?: string | null;
  readonly target_value?: string | null;
  readonly current_value?: string | null;
  readonly confidence_score?: string | null;
  readonly financial_impact_estimate?: string | null;
}

export interface BusinessOutcomeListParams {
  readonly limit: number;
  readonly offset: number;
  readonly owner_id?: string;
  readonly status?: readonly OutcomeStatus[];
  readonly target_before?: string;
  readonly target_after?: string;
  readonly search?: string;
}
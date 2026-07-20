export type KPIUnit =
  | "currency"
  | "percent"
  | "count"
  | "ratio"
  | "duration_seconds"
  | "duration_days"
  | "score";

export type KPIDirection = "increase" | "decrease" | "maintain";

export type KPIHealth = "on_track" | "at_risk" | "off_track" | "achieved";

export interface KPI {
  readonly id: string;
  readonly organization_id: string;
  readonly outcome_id: string | null;
  readonly owner_id: string | null;
  readonly name: string;
  readonly description: string | null;
  readonly unit: KPIUnit;
  readonly currency: string | null;
  readonly direction: KPIDirection;
  readonly baseline_value: string | number | null;
  readonly target_value: string | number | null;
  readonly current_value: string | number | null;
  readonly data_source: string | null;
  readonly refresh_frequency_hours: number | null;
  readonly is_active: boolean;
  readonly created_at: string;
  readonly updated_at: string;
}

export interface KPIOutcomeOption {
  readonly id: string;
  readonly organization_id: string;
  readonly name: string;
  readonly status: string;
}

export interface KPIOwnerOption {
  readonly id: string;
  readonly email: string;
  readonly full_name: string;
  readonly organization_id: string | null;
  readonly role: string;
  readonly status: string;
}

export interface PaginatedKPIs {
  readonly items: KPI[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedKPIOutcomes {
  readonly items: KPIOutcomeOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface PaginatedKPIOwners {
  readonly items: KPIOwnerOption[];
  readonly total: number;
  readonly limit: number;
  readonly offset: number;
}

export interface CreateKPIInput {
  readonly outcome_id?: string | null;
  readonly owner_id?: string | null;
  readonly name: string;
  readonly description?: string | null;
  readonly unit: KPIUnit;
  readonly currency?: string | null;
  readonly direction: KPIDirection;
  readonly baseline_value?: string | null;
  readonly target_value?: string | null;
  readonly current_value?: string | null;
  readonly data_source?: string | null;
  readonly refresh_frequency_hours?: number | null;
}

export interface UpdateKPIInput {
  readonly outcome_id?: string | null;
  readonly owner_id?: string | null;
  readonly name?: string;
  readonly description?: string | null;
  readonly direction?: KPIDirection;
  readonly baseline_value?: string | null;
  readonly target_value?: string | null;
  readonly current_value?: string | null;
  readonly data_source?: string | null;
  readonly refresh_frequency_hours?: number | null;
  readonly is_active?: boolean;
}

export interface KPIListParams {
  readonly limit: number;
  readonly offset: number;
  readonly outcome_id?: string;
  readonly owner_id?: string;
  readonly unit?: readonly KPIUnit[];
  readonly is_active?: boolean;
}
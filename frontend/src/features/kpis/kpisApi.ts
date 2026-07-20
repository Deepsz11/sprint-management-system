import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  CreateKPIInput,
  KPI,
  KPIListParams,
  PaginatedKPIOutcomes,
  PaginatedKPIOwners,
  PaginatedKPIs,
  UpdateKPIInput,
} from "./types";

function buildParams(params: KPIListParams): Record<string, unknown> {
  const query: Record<string, unknown> = {
    limit: params.limit,
    offset: params.offset,
  };
  if (params.outcome_id) query.outcome_id = params.outcome_id;
  if (params.owner_id) query.owner_id = params.owner_id;
  if (params.unit && params.unit.length > 0) {
    query.unit = [...params.unit];
  }
  if (typeof params.is_active === "boolean") {
    query.is_active = params.is_active;
  }
  return query;
}

export const kpisApi = {
  async list(params: KPIListParams): Promise<PaginatedKPIs> {
    const response = await apiClient.get<PaginatedKPIs>(API_ENDPOINTS.KPIS, {
      params: buildParams(params),
    });
    return response.data;
  },

  async get(id: string): Promise<KPI> {
    const response = await apiClient.get<KPI>(`${API_ENDPOINTS.KPIS}/${id}`);
    return response.data;
  },

  async create(input: CreateKPIInput): Promise<KPI> {
    const response = await apiClient.post<KPI>(API_ENDPOINTS.KPIS, input);
    return response.data;
  },

  async update(id: string, input: UpdateKPIInput): Promise<KPI> {
    const response = await apiClient.patch<KPI>(
      `${API_ENDPOINTS.KPIS}/${id}`,
      input,
    );
    return response.data;
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`${API_ENDPOINTS.KPIS}/${id}`);
  },

  async listOutcomes(): Promise<PaginatedKPIOutcomes> {
    const response = await apiClient.get<PaginatedKPIOutcomes>(
      API_ENDPOINTS.BUSINESS_OUTCOMES,
      { params: { limit: 200, offset: 0 } },
    );
    return response.data;
  },

  async listOwners(): Promise<PaginatedKPIOwners> {
    const response = await apiClient.get<PaginatedKPIOwners>(
      API_ENDPOINTS.USERS,
      { params: { limit: 200, offset: 0 } },
    );
    return response.data;
  },
};
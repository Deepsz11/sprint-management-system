import { apiClient } from "@/api/client";
import { API_ENDPOINTS } from "@/api/endpoints";

import type {
  BusinessOutcome,
  BusinessOutcomeListParams,
  CreateBusinessOutcomeInput,
  PaginatedBusinessOutcomes,
  PaginatedOutcomeKpis,
  PaginatedOutcomeOwners,
  PaginatedOutcomeProjects,
  UpdateBusinessOutcomeInput,
} from "./types";

function buildParams(
  params: BusinessOutcomeListParams,
): Record<string, unknown> {
  const query: Record<string, unknown> = {
    limit: params.limit,
    offset: params.offset,
  };
  if (params.owner_id) query.owner_id = params.owner_id;
  if (params.status && params.status.length > 0) {
    query.status = [...params.status];
  }
  if (params.target_before) query.target_before = params.target_before;
  if (params.target_after) query.target_after = params.target_after;
  if (params.search && params.search.trim().length > 0) {
    query.search = params.search.trim();
  }
  return query;
}

export const businessOutcomesApi = {
  async list(
    params: BusinessOutcomeListParams,
  ): Promise<PaginatedBusinessOutcomes> {
    const response = await apiClient.get<PaginatedBusinessOutcomes>(
      API_ENDPOINTS.BUSINESS_OUTCOMES,
      { params: buildParams(params) },
    );
    return response.data;
  },

  async create(input: CreateBusinessOutcomeInput): Promise<BusinessOutcome> {
    const response = await apiClient.post<BusinessOutcome>(
      API_ENDPOINTS.BUSINESS_OUTCOMES,
      input,
    );
    return response.data;
  },

  async update(
    id: string,
    input: UpdateBusinessOutcomeInput,
  ): Promise<BusinessOutcome> {
    const response = await apiClient.patch<BusinessOutcome>(
      `${API_ENDPOINTS.BUSINESS_OUTCOMES}/${id}`,
      input,
    );
    return response.data;
  },

  async remove(id: string): Promise<void> {
    await apiClient.delete(`${API_ENDPOINTS.BUSINESS_OUTCOMES}/${id}`);
  },

  async listProjects(): Promise<PaginatedOutcomeProjects> {
    const response = await apiClient.get<PaginatedOutcomeProjects>(
      API_ENDPOINTS.PROJECTS,
      { params: { limit: 200, offset: 0, include_archived: false } },
    );
    return response.data;
  },

  async listOwners(): Promise<PaginatedOutcomeOwners> {
    const response = await apiClient.get<PaginatedOutcomeOwners>(
      API_ENDPOINTS.USERS,
      { params: { limit: 200, offset: 0 } },
    );
    return response.data;
  },

  async listKpis(outcomeId?: string): Promise<PaginatedOutcomeKpis> {
    const params: Record<string, unknown> = { limit: 200, offset: 0 };
    if (outcomeId) params.outcome_id = outcomeId;
    const response = await apiClient.get<PaginatedOutcomeKpis>(
      API_ENDPOINTS.KPIS,
      { params },
    );
    return response.data;
  },
};